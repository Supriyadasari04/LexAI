from chatbot import ChatBot
from sentiment_analysis import EmotionRecognizer
from chat_summarizer import ChatSummarizer

def chat_main():
    bot = ChatBot()
    recognizer = EmotionRecognizer()
    summarizer = ChatSummarizer()

    print("\n⚖️ Welcome to Legal AI Chatbot! Type 'exit' to stop the conversation.\n")
    print(bot.intro_message)  # Display the introduction message
    
    # Ensure user details are collected before starting the chat
    bot.collect_basic_info()

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            print("\nLex: Thank you for sharing the details. The advocate will review your case. Have a great day!")
            break

        response = bot.get_response(user_input)
        print("\nLex:", response)

        # Save chat to history for summarization
        bot.chat_history.append({"user": user_input, "bot": response})  # Store chat
        bot.save_chat_history()  # Save chat history to file

    # Perform sentiment analysis on chat history
    bot.chat_history = bot.load_chat_history()
    sentiment_result = recognizer.analyze_overall_emotion()
    print(f"\n📊 Sentiment Analysis Result: {sentiment_result['overall_emotion']} (Score: {sentiment_result['sentiment_score']:.2f})\n")

    # Summarize chat history and display summary
    chat_summary = summarizer.summarize_chat()
    print("\n📄 Chat Summary:\n", chat_summary)

if __name__ == "__main__":
    chat_main()
