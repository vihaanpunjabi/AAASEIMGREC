import google.generativeai as genai
import os
from typing import Type
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def analyze_image(image_file, prompt, response_schema=None):

    model = genai.GenerativeModel('gemini-2.0-flash')
    image = genai.upload_file(image_file)
    
    if response_schema:
        response = model.generate_content(
            [prompt, image],
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=response_schema
            )
        )
    else:
        response = model.generate_content([prompt, image])
    
    return response.text





# EXAMPLE BELOW

class ImageAnalysis(BaseModel):
    label: str

with open("prompts/prompt.md", 'r') as f:
    prompt = f.read()

result = analyze_image("images/broken_laptop.jpeg", prompt, ImageAnalysis)
print("Result: ", result)

