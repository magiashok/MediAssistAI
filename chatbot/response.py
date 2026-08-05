from chatbot.groq_client import client
from chatbot.prompts import SYSTEM_PROMPT

def get_ai_response(messages):
    conversation = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    conversation.extend(messages)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=conversation,
        temperature=0.7,
        max_tokens=500,
    )

    return response.choices[0].message.content