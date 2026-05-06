import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_ai(context, question):
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