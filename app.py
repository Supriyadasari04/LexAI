import streamlit as st 
import uuid
import json
from assistant import get_chatbot
from datetime import datetime
from docs import document_summarizer_ui

page = st.sidebar.radio("📂 Select Page", ["🧑‍⚖️ Chat with Lex", "📜 Legal Document Summarizer"])

# CHAT PAGE 
if page == "🧑‍⚖️ Chat with Lex":
    # Initialize the chatbot
    init_chat, chat_with_user, summarize_conversation = get_chatbot()

    # Title and introduction
    st.title("Lex - Your Legal Assistant")
    st.markdown("""
        **Hi, I am Lex, your legal assistant for an advocate.**
        I am here to help you with collecting the details like Name, Gender, Occupation, and the reason for your legal consultation.
        You can start typing your message to initiate the chat.
    """)

    # Initialize session state variables if not present
    if "messages" not in st.session_state:
        st.session_state.messages = init_chat()
        st.session_state.user_input = ""

    # Input field for the user
    user_input = st.text_input("Your message:")

    if user_input:
        response, st.session_state.messages = chat_with_user(st.session_state.messages, user_input)
        st.session_state.user_input = user_input

        # Display assistant's response
        st.markdown(f"**Lex (Assistant):** {response}")

    # Appointment scheduling + summary saving
    with st.expander("📅 Schedule Appointment & Submit Conversation"):
        st.markdown("Please provide your contact and preferred appointment details.")

        email = st.text_input("Your Email")
        phone = st.text_input("Your Phone Number")
        preferred_date = st.date_input("Preferred Appointment Date")

        if st.button("Schedule Appointment"):
            if not email or not phone:
                st.warning("Please fill out all contact fields before submitting.")
            else:
                # summary generation
                summary = summarize_conversation(st.session_state.messages)

                # Generatin a unique case ID
                case_id = str(uuid.uuid4())

                # full summary data
                summary_data = {
                    "case_id": case_id,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "summary": summary,
                    "email": email,
                    "phone": phone,
                    "preferred_date": str(preferred_date)
                }

                # Save the summary + user details
                try:
                    with open("summaries.json", "r") as file:
                        summaries = json.load(file)
                except (FileNotFoundError, json.JSONDecodeError):
                    summaries = []

                summaries.append(summary_data)

                with open("summaries.json", "w") as file:
                    json.dump(summaries, file, indent=4)

                st.success(f"Appointment Request and conversation saved successfully! Case ID : {case_id}")

    # Display conversation history
    if st.session_state.messages:
        st.subheader("Conversation History")
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"**You:** {message['content']}")
            elif message["role"] == "assistant":
                st.markdown(f"**Lex (Assistant):** {message['content']}")

# DOCUMENT SUMMARIZER PAGE
elif page == "📜 Legal Document Summarizer":
    document_summarizer_ui()
