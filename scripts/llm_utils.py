from langchain_openai import ChatOpenAI

def get_gpt():
    return ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.8)
