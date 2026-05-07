import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def ask_ai(context, question):
  api_key = os.getenv("GROQ_API_KEY")

  if not api_key:
      return "Mock AI response"

  client = Groq(api_key=api_key)
  
  try:
    prompt = f"""
    Answer the question based only on the context below.

    Context:
    {context[:12000]}

    Question:
    {question}
    """

    response = client.chat.completions.create(
      model="llama-3.1-8b-instant",
      messages=[
          {"role": "user", "content": prompt}
      ]
    )

    return response.choices[0].message.content

  except Exception as e:
    return f"Error: {str(e)}"