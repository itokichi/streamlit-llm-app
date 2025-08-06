from dotenv import load_dotenv
import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# .envからAPIキーを読み込む
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# LLMからの回答を取得する関数
def get_llm_response(user_input: str, expert_type: str) -> str:
    # 専門家ごとのシステムメッセージ
    expert_messages = {
        "医療の専門家": "あなたは優秀な医療の専門家です。専門的かつ分かりやすく回答してください。",
        "法律の専門家": "あなたは信頼できる法律の専門家です。法的観点から分かりやすく回答してください。",
        "ITの専門家": "あなたは経験豊富なITの専門家です。技術的な観点から分かりやすく回答してください。"
    }
    system_message = expert_messages.get(expert_type, "あなたは親切なアシスタントです。")
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0,
        openai_api_key=openai_api_key
    )
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=user_input)
    ]
    result = llm(messages)
    return result.content

# Streamlitアプリ
st.title("専門家AIチャット（LangChain × Streamlit）")
st.write("""
このアプリは、あなたの質問に対して選択した分野の専門家としてAIが回答します。  
1. 専門家の種類を選択  
2. 質問を入力して送信  
AIが専門的な視点で回答します。
""")

# 専門家の種類を選択
expert_type = st.radio(
    "AIに振る舞わせる専門家を選んでください",
    ("医療の専門家", "法律の専門家", "ITの専門家")
)

# 入力フォーム
user_input = st.text_area("質問を入力してください", height=100)

if st.button("送信"):
    if user_input.strip() == "":
        st.warning("質問を入力してください。")
    else:
        with st.spinner("AIが回答中..."):
            response = get_llm_response(user_input, expert_type)
        st.markdown("#### 回答")
        st.write(response)