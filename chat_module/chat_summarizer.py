import os
import json
import groq

class ChatSummarizer:
    def __init__(self, model_name="llama3-8b-8192", chat_history_file="chat_history.json",
                 api_key="your_api_here"):
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

        prompt = f"""
        You are a legal assistant summarizing a conversation between a client and an AI assistant. 
        Your task is to provide a **concise and structured summary** of the client's details and their case **without adding any extra commentary or unnecessary information**.
        
        **Important Guidelines:**
        1. **Extract only relevant case details**—do not fabricate or interpret anything beyond what the user has stated.
        2. **Do NOT add assumptions, legal advice, or any AI-generated filler text.**
        3. **Structure the summary as follows:**
            - **Client’s Name, Gender, and Occupation:** Extracted from the chat.
            - **Client’s Issue:** Clearly summarize the legal concern they described.
            - **Key Details Provided:** Mention only essential information that would help the advocate assess the case.
            - **Additional Notes (if applicable):** If the client mentioned any deadlines, evidence, or specific concerns.

        **Chat Transcript:**
        {chat_text}
        """

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
