from google import genai
from dotenv import load_dotenv
from google.genai.errors import ServerError
import time
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


def generate_prompt(prompt_pre , data):
    arr = list(data.get("data"))
    def get_titles(entry):
        item = entry.get("node")
        title = item.get("title")
        return title
    
    x = map(get_titles, arr)
    titles = ", ".join(str(element) for element in x)

    prompt = f"{prompt_pre} {titles}, reply as if you are talking to the person"
    return prompt




def call_llm(prompt: str, retries = 3, delay =5):
    for i in range(3):
        try: 
            response = gemini(prompt)
            return response
        
        except ServerError as e:
            print("LLM server Busy, retrying")
            time.sleep(delay)
        
    return None
    
   

print("_client exists:", "_client" in globals())

