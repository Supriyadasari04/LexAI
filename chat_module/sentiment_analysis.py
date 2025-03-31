import json
from textblob import TextBlob
import os

class EmotionRecognizer:
    def __init__(self, chat_history_file="chat_history.json"):
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
                        else:
                            print("⚠ Chat history is corrupted. Resetting to empty list.")
                            return []
                    else:
                        print("⚠ Invalid chat history format. Resetting to empty list.")
                        return []
            except json.JSONDecodeError:
                print("Error reading chat history. Resetting to empty list.")
                return []
        return []

    def analyze_overall_emotion(self):

        if not isinstance(self.chat_history, list):
            return "Chat history is not in a valid list format."

        # Extract user messages safely
        user_texts = [chat.get("user", "") for chat in self.chat_history if isinstance(chat, dict) and "user" in chat]

        if not user_texts:
            return {"overall_emotion": "No user messages found", "sentiment_score": 0.0}

        combined_text = " ".join(user_texts)  # Merge all messages into one text block
        analysis = TextBlob(combined_text)
        polarity = analysis.sentiment.polarity

        # Determine overall emotion
        if polarity < -0.2:
            overall_emotion = "Negative (Urgent Attention Needed)"
        elif polarity > 0.2:
            overall_emotion = "Positive (Calm, Less Urgent)"
        else:
            overall_emotion = "Neutral (Moderate Attention Required)"

        return {
            "overall_emotion": overall_emotion,
            "sentiment_score": round(polarity, 2)
        }

if __name__ == "__main__":
    recognizer = EmotionRecognizer()
    
    result = recognizer.analyze_overall_emotion()
    print(f"Overall Emotion: {result['overall_emotion']} | Sentiment Score: {result['sentiment_score']:.2f}")
