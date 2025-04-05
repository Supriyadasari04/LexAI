# ⚖️ LexAI - Your Smart Legal Assistant

**LexAI** is an AI-powered legal assistant designed to streamline and simplify the day-to-day workflow of advocates and legal professionals.

At its core, LexAI is built to **intelligently handle client consultations**, **extract key insights**, and help advocates **prioritize their workload** with precision.

## 🧠 Key Capabilities

- **Conversational Intake**: LexAI interacts with clients in a chat-based format to gather essential details like name, gender, occupation, and the reason for seeking legal help.
  
- **Automated Case Summarization**: After the conversation, LexAI generates a concise and structured summary of the interaction, highlighting critical information about the case.

- **Smart Case Management Dashboard**: All client summaries are stored and visualized in a dynamic advocate dashboard. The dashboard allows for:
  - 🔍 Searching cases by email or case ID
  - 📅 Sorting cases by appointment date
  - 🟡 Filtering by case status (e.g., Pending, Reviewed, Accepted)
  - ✅ Quick actions like “Mark as Reviewed”

- **Document Summarization Module**: LexAI also allows users to upload legal documents (PDFs). The tool uses **OCR (if needed)** and **open-source language models** (`facebook/bart-large-cnn`) to generate a client-friendly summary of the document—perfect for quick insights on lengthy contracts or case files.

## 🎯 Purpose

The purpose of LexAI is to reduce the manual burden on advocates by:
- Automating the **client intake** and **summary documentation**
- Offering a centralized system to **view, filter, and manage client cases**
- Providing tools for **quick comprehension** of lengthy legal documents

---

## 🚀 Tech Stack

| Tool/Library       | Purpose                                           |
|--------------------|---------------------------------------------------|
| **Streamlit**      | Frontend web interface                            |
| **OpenAI + Groq**  | Language model for chat                           |
| **Hugging Face Transformers**      | For summarization model           |
| **pdfplumber**     | Extract text from PDFs                            |
| **pytesseract**    | OCR for scanned documents                         |
| **Pillow (PIL)**   | Image processing                                  |
| **Python**         | Entire Script handling                            |

---

## 📁 Project Structure

```bash
📦 LexAI
├── app.py                  # Main User focused Streamlit app (UI & Navigation)
├── adv.py                  # Advocate focused Streamlit Dashboard (UI & Navigation)
├── assistant.py            # Chat assistant logic (prompt, response)
├── docs.py                 # Legal document OCR + summarization logic
├── summaries.json          # Saved case details & summaries (auto-generated)
├── requirements.txt        # Python dependencies & libraries necessary
└── README.md               # Project documentation
```

---
## 🔐 API Usage

- For Chat Assistant: You'll need a groq API key. You can get one from here - [https://console.groq.com]
- For Summarization: The summarizer in `docs.py` uses Hugging Face Transformers and the model `facebook/bart-large-cnn`. No need to install or generate any API for this.

---
## 🛠️ Steps to run
1. Clone the repo:
   ```
   git clone https://github.com/Keerthanareddy17/LexAI.git
   cd LexAI
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Paste your groq API key generated in the designated space within the `assitant.py` file.
4. Run the app:
   - Try the user end and start chatting with LEX-
     ```
     streamlit run app.py
      ```
   - For the advocate dahsboard -
     ```
     streamlit run adv.py
     ```
   - Upload a PDF and get the summaries

---

🔮 Future Improvements
- ✨ Multi-language legal document support
- 🔐 Login system for advocates and clients
- 📁 Integration with cloud storage (Google Drive, Dropbox, etc.)
- 📅 Calendar sync for appointment scheduling

---

Feel free to reach out for feedback or queries -
📧 Email: katasanikeerthanareddy@gmail.com

🔗 LinkedIn: [linkedin.com/in/keerthana-reddy-katasani-b07238268](https://www.linkedin.com/in/keerthana-reddy-katasani-b07238268/)

---
## 📷 Snapshots of LexAI

![Screenshot 2025-04-05 163904](https://github.com/user-attachments/assets/00fc6ed8-51f1-4297-bd1b-5178822274f6)

![Screenshot 2025-04-05 164147](https://github.com/user-attachments/assets/a4de7712-c6a3-4465-9f40-8b046a95ebf3)

![Screenshot 2025-04-05 164247](https://github.com/user-attachments/assets/e35d0ce9-2cbf-4e27-9bb0-7fac2f60cf3e)

![Screenshot 2025-04-05 164322](https://github.com/user-attachments/assets/dd5b06b6-a247-4c16-ae5b-4345e4bb6342)

![Screenshot 2025-04-05 165208](https://github.com/user-attachments/assets/b1861adc-22f6-4dd1-9cfe-17a18202f60c)










   


