import google.generativeai as genai

api_key='AIzaSyC3N6bbu0b-Gd3c1DIQCeJLwawSwjcH50c'
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 100,
    "max_output_tokens": 32768,
}

url =f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=api_key'


model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)