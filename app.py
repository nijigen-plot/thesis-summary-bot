import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()
from pdf_summary import Summary

summary_instance = Summary()

st.title("PDF 要約BOT")
st.subheader("なが～い論文等のPDFを日本語で要約！")

uploaded_file = st.file_uploader(
    "PDFファイルをアップロードしてください。",
    type=["pdf"],
    key="pdf_upload"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if uploaded_file is not None:
    try:
        with st.spinner("要約中..."):
            pdf = uploaded_file.read()
            response = summary_instance.generate_message(pdf)

            with st.chat_message("assistant"):
                st.markdown(str(response))
    
    except Exception as e:
        st.error(f"予期しないエラーが発生しました: {e}")