import os
import pathlib
import textwrap

import google.generativeai as genai
GOOGLE_API_KEY=api_key = os.getenv("GOOGLE_API_KEY")

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("What is the meaning of life?")
print(response.text)

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])
chat
response = chat.send_message("In one sentence, explain how a computer works to a young child.")
print(response.text)


model = genai.GenerativeModel('gemini-pro')

messages = [
    {'role':'user',
     'parts': ["Briefly explain how a computer works to a young child."]}
]
response = model.generate_content(messages)

print(response.text)
messages.append({'role':'model',
                 'parts':[response.text]})

messages.append({'role':'user',
                 'parts':["Okay, how about a more detailed explanation to a high school student?"]})

response = model.generate_content(messages)

print(response.text)

