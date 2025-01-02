import google.generativeai as genai
import markdown
from bs4 import BeautifulSoup # pip install beautifulsoup4
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')


class aGPT():
    def __init__(self):
        model = genai.GenerativeModel("gemini-1.5-flash")
        genai.configure(api_key=GOOGLE_API_KEY)
        self.chat = model.start_chat(
            history=[
                {"role": "user", "parts": "Hello"},
                {"role": "model", "parts": "Great to meet you. What would you like to know?"},
            ]   
        )

    def ask(self,text):
        response = self.chat.send_message(text)
        # head_response = chat.send_message("Can you please share the searchable title for this in one line? it should be maximum 60 characters")
        gen_text_obj = BeautifulSoup(markdown.markdown(response.text), features='html.parser')
        gen_text = gen_text_obj.get_text()
        # print()
        return gen_text 
    