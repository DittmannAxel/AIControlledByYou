from llm_query import generate_sql_from_text

def test_llm_connectivity():
    sample_query = "Give me the last 10 motor RPM values"
    sql = generate_sql_from_text(sample_query)
    print("LLM generated SQL:")
    print(sql)

if __name__ == "__main__":
    test_llm_connectivity()