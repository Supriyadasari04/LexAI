# 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

from openai import OpenAI

def get_chatbot():
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key="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"
    )

    SYSTEM_PROMPT = """
    You are LexAI, a friendly legal assistant. Follow these steps:
    1. Introduce yourself briefly
    2. Ask for client's name, gender, and occupation
    3. Ask about their legal concern
    4. Summarize the information
    Be professional but warm. Never give legal advice.
    """

    def init_chat():
        return [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "assistant", "content": "Hello! I'm LexAI, your legal assistant. May I know your name?"}
        ]

    def chat_with_user(messages, user_input):
        messages.append({"role": "user", "content": user_input})
        
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        assistant_reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_reply})
        return assistant_reply, messages

    def summarize_conversation(messages):
        summary_prompt = """
        Create a client summary with:
        1. Name, Gender, Occupation
        2. Legal concern (50 words max)
        """
        summary_messages = messages + [{"role": "user", "content": summary_prompt}]
        
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=summary_messages,
            temperature=0.3,
            max_tokens=200
        )
        return response.choices[0].message.content

    return init_chat, chat_with_user, summarize_conversation