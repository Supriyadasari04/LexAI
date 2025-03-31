import os
import json
import groq

class ChatSummarizer:
    def __init__(self, model_name="llama3-8b-8192", chat_history_file="chat_history.json",
                 api_key="your_api_key"):
        self.client = groq.Client(api_key=api_key)
        self.model_name = model_name
        self.chat_history_file = chat_history_file
        self.chat_history = self.load_chat_history()

    def load_chat_history(self):
        """Loads the chat history from a JSON file and ensures correct format."""
        if os.path.exists(self.chat_history_file):
            try:
                with open(self.chat_history_file, "r", encoding="utf-8") as file:
                    data = json.load(file)

                    # Ensure correct JSON structure
                    if isinstance(data, dict) and "chat_history" in data:
                        chat_history = data["chat_history"]

                        # Ensure chat_history is a list of dictionaries
                        if isinstance(chat_history, list) and all(isinstance(entry, dict) for entry in chat_history):
                            return chat_history  
            except json.JSONDecodeError:
                pass  # If error occurs, return empty list
        
        return []  # Default to empty list if file is missing or corrupted

    def summarize_chat(self):
        """Summarizes the entire chat history using Groq API."""
        if not self.chat_history:
            return "No chat history found."

        try:
            chat_text = "\n".join(
                [f"User: {chat.get('user', 'N/A')}\nBot: {chat.get('bot', 'N/A')}" 
                 for chat in self.chat_history if isinstance(chat, dict)]
            )
        except TypeError:
            return "Invalid chat format."

        # Prevent making API calls with empty data
        if not chat_text.strip():
            return "No valid user-bot exchanges found in chat history."

        prompt = (
    "You are a legal assistant summarizing a chat between a client and an advocate."
    "Act very professional and Provide a structured summary in a format that allows the advocate to quickly grasp the case details. Don't add any other additional lines other than the summary"
    "Ensure clarity and conciseness. Structure the summary as follows:\n\n"
    "**Client's Name and Gender along with occupation:**\n"
    "**Client's Issue:** (Briefly describe the main concern of the client.)\n"
    "Here is the chat transcript:\n\n"
    f"{chat_text}"
)


        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except Exception:
            return "Error: Unable to summarize the chat at this moment."

# Example Usage
if __name__ == "__main__":
    summarizer = ChatSummarizer()
    print("📄 Chat Summary:\n", summarizer.summarize_chat())
