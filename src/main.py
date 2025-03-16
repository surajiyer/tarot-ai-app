import streamlit as st

chat_page = st.Page("chat.py", title="Chat", icon="💬")
pg = st.navigation([chat_page])
pg.run()
