from google import genai
from dotenv import load_dotenv

load_dotenv()


_client = None

def gemini(prompt:str):
    client = get_client()
    response = client.models.generate_content(
        model="gemini-3-flash-preview", contents=prompt
    )
    return response


def get_client():
    global _client
    if _client is None:
        _client = genai.Client()
    return _client


def generate_prompt(data):
    arr = list(data.get("data"))
    def get_titles(entry):
        item = entry.get("node")
        title = item.get("title")
        return title
    
    x = map(get_titles, arr)
    titles = ", ".join(str(element) for element in x)

    prompt = f"You are a personality assessor, Based on Psychological studies from the web and based on your data, give insights into the personality of person who likes the following anime {titles}, reply as if you are talking to the person"
    return prompt




def call_llm(prompt: str):
    response = gemini(prompt)
    print(response.text)
    return response.text

print("_client exists:", "_client" in globals())

