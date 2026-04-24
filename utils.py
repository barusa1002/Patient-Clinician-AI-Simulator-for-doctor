# utils.py
import re
import streamlit as st

# ==========================================================
# フィルタ関数
# ==========================================================
def strip_thought(text: str) -> str:
    if not text:
        return text

    text = re.sub(r"THOUGHT.*?回答[:：]", "", text, flags=re.DOTALL)
    text = re.sub(r"THOUGHT.*", "", text)
    text = re.sub(r"回答[:：]", "", text)

    if "発話：" in text:
        text = text.split("発話：")[-1]

    return text.strip()


# ==========================================================
# モバイル判定関数
# ==========================================================
MOBILE_KEYWORDS = ["iphone", "android", "ipad", "mobile", "blackberry", "windows phone"]

def detect_mobile() -> bool:
    try:
        user_agent = st.context.headers.get("user-agent", "").lower()
        return any(keyword in user_agent for keyword in MOBILE_KEYWORDS)
    except Exception:
        return False


# ==========================================================
# セッションリセット関数
# ==========================================================
def reset_session():
    for key in ["chat_history", "chat_session", "current_scenario"]:
        if key in st.session_state:
            del st.session_state[key]
