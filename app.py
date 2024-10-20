# main.py
import streamlit as st  # type: ignore
from api_server import run_fastapi
import threading
from views import show_ranking, show_logs, show_management
import time


def main():
    st.set_page_config(page_title="Quiz Admin Dashboard", layout="wide")

    # Start FastAPI server in a separate thread
    api_thread = threading.Thread(target=run_fastapi, daemon=True)
    api_thread.start()
    time.sleep(2)  # Give FastAPI time to start

    st.title("Quiz Admin Dashboard")

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Rankings", "Logs", "Player Management"])

    if page == "Rankings":
        show_ranking()
    elif page == "Logs":
        show_logs()
    elif page == "Player Management":
        show_management()

    # Display API status
    st.sidebar.markdown("---")
    st.sidebar.write("API Status:")
    st.sidebar.info("✅ FastAPI Server running on http://127.0.0.1:8081")


if __name__ == "__main__":
    main()
