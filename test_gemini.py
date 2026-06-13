import google.generativeai as genai

genai.configure(api_key="YOUR_GEMINI_API_KEY")

model = genai.GenerativeModel("gemini-2.5-flash")

response = model.generate_content(
    "Say hello and tell me the capital of India."
)

print(response.text)