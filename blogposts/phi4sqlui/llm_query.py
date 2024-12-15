import os
import json
import ssl
import urllib.request
from dotenv import load_dotenv
import re

load_dotenv()

ENDPOINT = os.getenv("AZURE_ENDPOINT")
API_KEY = os.getenv("AZURE_API_KEY")

def allowSelfSignedHttps(allowed):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True)

def generate_sql_from_text(user_query: str) -> str:
    if not API_KEY:
        raise Exception("A key should be provided to invoke the endpoint")

    data = {
        "input_data": {
            "input_string": [
                {
                    "role": "user",
                    "content": f"User wants: {user_query}. Return a valid SQL query on the sensor_data table. Make sure to return only the SQL statement, no additional text. Do not start with sql -just the plain sql statement - no additions!!Return only the raw SQL statement without any code fences or formatting blocks. Do not prepend ‘sql’ or any other text, just the SQL itself."
                }
            ],
            "parameters": {
                "max_new_tokens": 4096
            }
        }
    }

    body = str.encode(json.dumps(data))
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }

    req = urllib.request.Request(ENDPOINT, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        result_data = json.loads(result)

        output = result_data.get("output", "").strip()
        print("LLM response:", output)
        if not output:
            print("No valid 'output' field in LLM response.")
            return ""

        # Remove backticks or code fences if any:
        cleaned_sql = re.sub(r"```(sql)?```", "", output, flags=re.IGNORECASE)
        cleaned_sql = re.sub(r"```(\s*sql\s*)?", "", output, flags=re.IGNORECASE)
        cleaned_sql = cleaned_sql.strip('`').strip()

        print("LLM generated SQL:", cleaned_sql)
        return cleaned_sql
    except urllib.error.HTTPError as error:
        print("LLM request failed:", error)
        return ""