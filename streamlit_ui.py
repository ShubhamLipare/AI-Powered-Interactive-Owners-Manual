import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"

st.set_page_config(
    page_title="AI Interactive Owner’s Manual",
    layout="wide"
)

# --------------------------------------------------
# Helpers
# --------------------------------------------------
def set_page(page_name: str):
    st.query_params.clear()
    st.query_params["page"] = page_name
    st.rerun()

def get_page():
    page = st.query_params.get("page", "home")
    if isinstance(page, list):
        page = page[0]
    return page

# --------------------------------------------------
# Session State
# --------------------------------------------------
if "retriever_ready" not in st.session_state:
    st.session_state.retriever_ready = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --------------------------------------------------
# Navigation
# --------------------------------------------------
with st.sidebar:
    st.header("📘 Navigation")

    if st.button("🏠 Home"):
        set_page("home")

    if st.button("📂 Ingest Documents"):
        set_page("ingest")

    if st.button("💬 Chat"):
        set_page("chat")

# --------------------------------------------------
# Routing
# --------------------------------------------------
page = get_page()

# ==================================================
# HOME
# ==================================================
if page == "home":
    st.title("📘 AI-Powered Interactive Owner’s Manual")
    st.markdown("""
    ### What you can do:
    - Upload manuals
    - Ingest documents
    - Chat with AI
    """)

# ==================================================
# INGEST
# ==================================================
elif page == "ingest":
    st.title("📂 Document Ingestion")

    uploaded_files = st.file_uploader(
        "Upload one or more documents",
        accept_multiple_files=True
    )

    if st.button("🚀 Ingest Documents"):
        if not uploaded_files:
            st.warning("Please upload at least one document.")
        else:
            with st.spinner("Ingesting documents..."):
                files_payload = [
                (
                    "files", (f.name, f.getbuffer(), "application/pdf")
                ) for f in uploaded_files
                ]

                response = requests.post(
                    f"{BACKEND_URL}/ingest",
                    files=files_payload,
                    timeout=120
                )

            if response.status_code == 200:
                st.session_state.retriever_ready = True
                st.success("✅ Documents ingested successfully!")
            else:
                st.error("❌ Ingestion failed.")

# ==================================================
# CHAT
# ==================================================
elif page == "chat":
    st.title("💬 Chat with Your Manual")

    if not st.session_state.retriever_ready:
        st.warning("Please ingest documents first.")
        st.stop()

    user_query = st.chat_input("Ask a question...")

    if user_query:
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json={"query": user_query,"chat_history":st.session_state.chat_history},
            timeout=60
        )

        if response.status_code == 200:
            ai_answer = response.json()["response"]
            st.session_state.chat_history.append({
                "user": user_query,
                "ai": ai_answer
            })
        else:
            st.error("Backend error.")

    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(chat["user"])
        with st.chat_message("assistant"):
            st.write(chat["ai"])
