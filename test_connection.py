from langchain_openai import ChatOpenAI

# Update the port if you are using LM Studio (1234) instead of Ollama (11434)
llm = ChatOpenAI(
    base_url="http://localhost:8080/v1", 
    api_key="lm-studio", 
    model="llama3" 
)

try:
    response = llm.invoke("Say 'Connection Successful!'")
    print(response.content)
except Exception as e:
    print(f"Error: {e}")