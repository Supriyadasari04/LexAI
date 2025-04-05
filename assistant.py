from openai import OpenAI

def get_chatbot():
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key="your_api_key" 
    )

    SYSTEM_PROMPT = (
        "You are Lex, a professional legal assistant for an advocate. "
        "Your role is to collect the following details from the client: Name, Gender, and Occupation. "
        "Then, continue the conversation to understand the reason for their legal consultation. "
        "Maintain context, be formal, and helpful. Never give legal advice or step out of your assistant role. "
        "Once you have gathered the required information and discussed the issue, inform the user that the advocate will "
        "review the summary of this conversation and decide whether to take up the case. "
        "End the conversation only after politely acknowledging that their case will be reviewed and they will be contacted later."
    )

    def init_chat():
        return [
            {"role": "system", "content": SYSTEM_PROMPT}
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
        summary_prompt = (
            "Summarize this conversation between a legal assistant and a client."
            " Focus on the user details collected and the legal concern discussed."
        )
        summary_messages = messages + [{"role": "user", "content": summary_prompt}]
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=summary_messages,
            temperature=0.3,
            max_tokens=300
        )
        return response.choices[0].message.content

    return init_chat, chat_with_user, summarize_conversation