# app.py
import streamlit as st
import pandas as pd
from groq import Groq
from datetime import datetime, timedelta
import os

# --- CONFIG ---
os.environ["GROQ_API_KEY"] = "PASTE YOUR API URL HERE FROM GROQ" #IMPORTANT 
client = Groq(api_key=os.environ["GROQ_API_KEY"])

st.set_page_config(page_title="Fyra Finlyze", page_icon="💸", layout="wide")

# --- PAGE TITLE ---
st.markdown(
    """
    <h1 style='color:#FFFFFF; text-align:center;'>💸 Fyra Finlyze — Your Smart Finance Assistant</h1>
    """,
    unsafe_allow_html=True
)

# --- FILE UPLOAD ---
uploaded_file = st.file_uploader(
    "📂 Upload your UPI/finance Excel file (.xlsx) with columns: Date, Category, Merchant, Amount (₹), Mode, Description",
    type=["xlsx"]
)

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # --- CLEAN DATA ---
    df = df.rename(columns={
        'Date': 'Date',
        'Category': 'Category',
        'Merchant': 'Merchant',
        'Amount (₹)': 'Amount',
        'Mode': 'Mode',
        'Description': 'Description'
    })

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date", "Amount"])
    df["Amount"] = df["Amount"].astype(float)

    # --- SUMMARY FUNCTION ---
    def generate_summary():
        summary = {
            "total_spent": round(df["Amount"].sum(), 2),
            "num_transactions": len(df),
            "top_categories": df.groupby("Category")["Amount"].sum().sort_values(ascending=False).head(5).to_dict(),
            "top_merchants": df.groupby("Merchant")["Amount"].sum().sort_values(ascending=False).head(5).to_dict(),
            "top_modes": df.groupby("Mode")["Amount"].sum().sort_values(ascending=False).to_dict(),
            "latest_date": df["Date"].max().strftime("%Y-%m-%d"),
            "earliest_date": df["Date"].min().strftime("%Y-%m-%d")
        }

        # Payment modes summary
        modes = ["upi", "gpay", "card", "cash", "wallet"]
        for mode in modes:
            mode_data = df[df["Mode"].str.lower().str.contains(mode, na=False)]
            summary[f"{mode}_transactions"] = len(mode_data)
            summary[f"{mode}_total_spent"] = round(mode_data["Amount"].sum(), 2)
        return summary

    # --- CLEAN RESPONSE ---
    def clean_response(text):
        return text.replace("**", "").replace("*", "")

    # --- CHAT FUNCTION ---
    def query_fyra(user_input):
        summary = generate_summary()
        user_lower = user_input.lower()

        # Direct mode queries
        modes = ["upi", "gpay", "card", "cash", "wallet"]
        for mode in modes:
            if mode in user_lower:
                if any(k in user_lower for k in ["transaction", "transactions", "count", "number"]):
                    return f"Total {mode.upper()} transactions: {summary.get(f'{mode}_transactions', 0)}"
                elif any(k in user_lower for k in ["spend", "spent", "amount", "total"]):
                    return f"Total {mode.upper()} spending: ₹{summary.get(f'{mode}_total_spent', 0):,.2f}"
                else:
                    return (
                        f"Total {mode.upper()} transactions: {summary.get(f'{mode}_transactions', 0)}\n"
                        f"Total {mode.upper()} spending: ₹{summary.get(f'{mode}_total_spent', 0):,.2f}"
                    )

        # Otherwise use Groq LLM
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant", #IMPORTANT  #IF THIS MODEL GET DECOMISSIONED , GET A NEW WORKINGMODEL FROM GROQ
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Fyra Finlyze — a smart personal finance assistant. "
                        "You analyze spending data from a dataset with columns: Date, Category, Merchant, Amount, Mode, Description. "
                        "You understand natural human queries, typos, informal text, and can answer totals, category spending, merchant queries, mode queries, description queries, time-based queries, highest/lowest spending, averages, comparisons, and casual/fun questions. "
                        "Always include ₹ for amounts. If unsure, make best guess based on dataset."
                    ),
                },
                {"role": "system", "content": f"Dataset summary: {summary}"},
                {"role": "user", "content": user_input},
            ],
            temperature=0.3,
            max_tokens=800,
        )
        return clean_response(response.choices[0].message.content.strip())

    # --- CHAT UI ---
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    user_input = st.text_input("💬 Type your question:", key="user_input")

    if st.button("Send") and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        answer = query_fyra(user_input)
        st.session_state.messages.append({"role": "assistant", "content": answer})

    # --- DISPLAY CHAT ---
    for msg in st.session_state.messages:
        # User messages (green left boxes)
        if msg["role"] == "user":
            st.markdown(
                f"""
                <div style='text-align:left; background-color:#4b5320; color:white;
                padding:10px; border-radius:10px; margin:8px 0; width:fit-content;'>
                <b>You:</b> {msg['content']}
                </div>
                """,
                unsafe_allow_html=True,
            )
        # Assistant messages (gray left boxes)
        else:
            st.markdown(
                f"""
                <div style='text-align:left; background-color:#2f2f2f; color:#a4ffaf;
                padding:10px; border-radius:10px; margin:8px 0; width:fit-content;'>
                <b>Fyra Finlyze:</b> {msg['content']}
                </div>
                """,
                unsafe_allow_html=True,
            )

else:
    st.info("📤 Please upload your Excel file to start chatting with Fyra Finlyze!")
