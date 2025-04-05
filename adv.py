import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="Lex Advocate Dashboard", layout="wide")
st.title("📂 Lex - Advocate Dashboard")

st.markdown("Search, filter, and manage all submitted case summaries below.")

def load_summaries():
    if os.path.exists("summaries.json"):
        with open("summaries.json", "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_summaries(data):
    with open("summaries.json", "w") as file:
        json.dump(data, file, indent=4)

summaries = load_summaries()

for s in summaries:
    if "status" not in s:
        s["status"] = "Pending"

#Sidebar Filters
st.sidebar.header("🔎 Filters")

search_query = st.sidebar.text_input("Search by Email or Case ID")
status_filter = st.sidebar.selectbox("Filter by Status", ["All", "Pending", "Reviewed", "Accepted"])
sort_order = st.sidebar.selectbox("Sort by Date", ["Newest First", "Oldest First"])

# Apply Filters
if search_query:
    summaries = [
        s for s in summaries
        if search_query.lower() in s.get("email", "").lower() or search_query.lower() in s.get("case_id", "").lower()
    ]

if status_filter != "All":
    summaries = [s for s in summaries if s.get("status") == status_filter]

summaries.sort(
    key=lambda x: datetime.strptime(x["timestamp"], "%Y-%m-%d %H:%M:%S"),
    reverse=(sort_order == "Newest First")
)

# Display
if summaries:
    for idx, summary in enumerate(summaries):
        with st.expander(f"🧾 Case ID: {summary['case_id']} | {summary['timestamp']}"):
            st.markdown(f"**📝 Summary:** {summary['summary']}")
            st.markdown(f"**📧 Email:** {summary['email']}")
            st.markdown(f"**📱 Phone:** {summary['phone']}")
            st.markdown(f"**📆 Preferred Appointment Date:** {summary['preferred_date']}")
            st.markdown(f"**📌 Current Status:** `{summary['status']}`")

            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                if st.button("✅ Mark as Reviewed", key=f"reviewed_{summary['case_id']}"):
                    summaries[idx]["status"] = "Reviewed"
                    save_summaries(summaries)
                    st.success("Marked as Reviewed.")
            with col2:
                if st.button("✔️ Accept Case", key=f"accept_{summary['case_id']}"):
                    summaries[idx]["status"] = "Accepted"
                    save_summaries(summaries)
                    st.success("Case Accepted.")
else:
    st.info("No case summaries found matching the criteria.")
