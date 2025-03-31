import os
import json
import groq

class ChatBot:
    def __init__(self, model_name="llama3-8b-8192", chat_history_file="chat_history.json", api_key="your_api_key"):
        self.client = groq.Client(api_key=api_key)
        self.model_name = model_name
        self.chat_history_file = chat_history_file
        self.chat_history = self.load_chat_history()
        self.user_details = {}  # Stores user information
        self.case_details = {}  # Stores case-related details
        self.intro_message = (
            "\n🤖 Lex: Hello! I'm Lex, your legal assistant. Please note that I am **not a lawyer**, "
            "but I will collect important details for the advocate. This helps them decide if an appointment is needed.\n"
        )

    def load_chat_history(self):
        """Loads existing chat history from a JSON file, including user details and case details."""
        if os.path.exists(self.chat_history_file):
            with open(self.chat_history_file, "r") as file:
                data = json.load(file)
                self.user_details = data.get("user_details", {})  
                self.case_details = data.get("case_details", {})  
                return data.get("chat_history", [])  
        return []

    def save_chat_history(self):
        data = {
            "user_details": self.user_details,
            "case_details": self.case_details,
            "chat_history": self.chat_history
        }
        try:
            with open(self.chat_history_file, "w") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"⚠ Error saving chat history: {e}")  


    def collect_basic_info(self):
        """Ensures Name, Gender, and Occupation are collected before starting case discussion."""
        required_details = {
            "name": "May I know your name?",
            "gender": "How do you identify yourself? (Male/Female/Other)?",
            "occupation": "What is your occupation?",
        }

        for key, question in required_details.items():
            if key not in self.user_details:  # Avoid re-asking
                answer = input(f"🤖 Lex: {question}\nYou: ").strip()
                if answer:
                    self.user_details[key] = answer

        print(
            f"\n🤖 Lex: Thank you, {self.user_details['name']}! Let's discuss your case."
            " I will ask a few questions to help the advocate understand your situation.\n"
        )

    def get_response(self, user_input):
        #Generates chatbot response while maintaining context.
        # Ensure chat history is not empty before generating response
        prompt = f"""
        You are Lex, an AI legal assistant. Your job is ONLY to collect details about a case for an advocate.
        You are NOT a lawyer and must NOT provide legal advice. Your role is to help determine if an appointment is necessary.

        User Details Collected:
        - Name: {self.user_details.get('name', 'Not Provided')}
        - Gender: {self.user_details.get('gender', 'Not Provided')}
        - Occupation: {self.user_details.get('occupation', 'Not Provided')}

        Case Details Collected So Far:
        {json.dumps(self.case_details, indent=4)}

        Guidelines:
        1. If the user has already provided an answer, do NOT ask the same question again.
        2. Naturally guide the conversation by **asking for missing information**.
        3. Maintain context and ask only questions relevant to their discussion.
        4. **DO NOT give legal advice.** Instead, focus on gathering information for the advocate.
        5. Don't repeat the questions again and again.
        6. Keep asking if they have anything else to share.
        7. End the chat with a friendly closing message.

        User: {user_input}
        AI:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            reply = response.choices[0].message.content.strip()

            # Store conversation
            self.chat_history.append({"user": user_input, "bot": reply})
            self.save_chat_history()  # Save after every interaction

            return reply
        except Exception as e:
            return f" AI Error: {e}"

if __name__ == "__main__":
    bot = ChatBot()

    print(bot.intro_message)  
    bot.collect_basic_info()  

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            print("\n🤖 Lex: Thank you for sharing the details. The advocate will review your case. Have a great day!")
            break
        print("\n🤖 Lex:", bot.get_response(user_input))
