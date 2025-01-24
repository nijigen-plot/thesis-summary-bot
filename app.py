import base64
import os

import streamlit as st
from dotenv import load_dotenv

from logger_setup import setup_logger
from pdf_summary import Summary

logger = setup_logger()
load_dotenv()

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
            pdf_data = base64.standard_b64encode(pdf).decode('utf-8')
            response = summary_instance.generate_message(pdf_data)
            summary_text = response["text"]
            response['filename'] = uploaded_file.name
            logger.info(f"{response}")
            with st.chat_message("assistant"):
                st.markdown(summary_text)
    
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")