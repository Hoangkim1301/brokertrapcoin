import openai
import os

import configparser

config = configparser.ConfigParser()
config.read('config.ini')
openai_api_key = config.get('openai', 'api_key')
#nytimes_api_key = config.get('nytimes', 'api_key')

print(f"OpenAI API Key: {openai_api_key}")
#print(f"NY Times API Key: {nytimes_api_key}")

openai.api_key = openai_api_key

def chat(message):
    response = openai.Completion.create(
        model="gpt-3.5-turbo-1106", messages=messages 
    )
    
def check_api_key():
    # Make sure API key is set.
    if not os.environ.get("API_KEY"):
        raise RuntimeError("API_KEY not set")
    else:
        print("API_KEY is set")
    
messages = [ {"role": "system", "content":  
              "You are a intelligent assistant."} ] 
def interact():
    while True: 
        message = input("User : ") 
        if message: 
            messages.append( 
                {"role": "user", "content": message}, 
            ) 
            chat = openai.ChatCompletion.create( 
                model="gpt-3.5-turbo-1106", messages=messages 
            ) 
        reply = chat.choices[0].message.content 
        print(f"ChatGPT: {reply}") 
        messages.append({"role": "assistant", "content": reply}) 
        
if __name__ == "__main__":
    check_api_key()
    