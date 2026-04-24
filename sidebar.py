#sidebar.py
import streamlit as st
from utils import reset_session
from db import logout

# task_infoのキーとアイコンのマッピング
TASK_INFO_ICONS = {
    "課題内容": "📋",
    "患者情報": "👤",
    "学生情報": "🎓",
    "場面設定": "🏥",
    "医療従事者情報": "🧑‍⚕️",
    "処方内容": "💊",
}


def render_sidebar(
    SCENARIOS,
    SCENARIO_PROMPTS,
    current_datetime
):
    # ============================
    # 学習モード表示・切替
    # ============================
    learning_mode = st.session_state.get("learning_mode", "OSCE対策")
    st.sidebar.markdown(f"**🎓 学習モード：{learning_mode}**")
    if st.sidebar.button("🔀 学習モードを変更する"):
        keys_to_clear = ["learning_mode", "chat_history", "chat_session", "current_scenario"]
        for k in keys_to_clear:
            st.session_state.pop(k, None)
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.header("📝 課題設定")

    # ============================
    # 課題選択
    # ============================
    mode = st.sidebar.selectbox("モード", list(SCENARIOS.keys()))
    scenario = st.sidebar.selectbox("主訴・課題", SCENARIOS[mode])
    subscenario = st.sidebar.selectbox(
        "サブシナリオ",
        list(SCENARIO_PROMPTS[mode][scenario].keys())
    )

    selected = SCENARIO_PROMPTS[mode][scenario][subscenario]

    from datetime import datetime
    today = datetime.now().strftime("%Y年%m月%d日")

    task_info_display = {}
    for k, v in selected["task_info"].items():
        if isinstance(v, str):
            task_info_display[k] = v.replace("{{TODAY}}", today)
        else:
            task_info_display[k] = v

    # ============================
    # 課題詳細（折りたたみ）
    # ============================
    with st.sidebar.expander("📘 課題詳細", expanded=True):

        for key, value in task_info_display.items():
            icon = TASK_INFO_ICONS.get(key, "📌")
            st.markdown(f"### {icon} {key}")
            st.text(value)

        st.markdown(f"### 🕒 日時\n{current_datetime}")

    # ============================
    # セッションリセット
    # ============================
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 セッションをリセット"):
        reset_session()
        st.rerun()

    # ============================
    # AI評価
    # ============================
    st.sidebar.markdown("---")
    st.sidebar.subheader("📝 AI評価")

    if st.sidebar.button(
        "AIによる評価を実行",
        disabled=len(st.session_state.get("chat_history", [])) == 0
    ):
        st.session_state.run_evaluation = True

    # ============================
    # 設定
    # ============================
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ 設定")

    if st.sidebar.button("⚙️ ユーザー設定"):
        st.session_state.page = "settings"

    if st.sidebar.button("⬅ チャットに戻る"):
        st.session_state.page = "chat"

    # ============================
    # 教員専用
    # ============================
    if st.session_state.get("role") == "staff":
        st.sidebar.markdown("---")
        st.sidebar.subheader("👨‍🏫 教員メニュー")

        if st.sidebar.button("📊 学生評価一覧"):
            st.session_state.page = "staff_dashboard"
            st.rerun()

    # ============================
    # ログイン情報
    # ============================
    st.sidebar.markdown("---")

    with st.sidebar.expander("👤 ログイン情報", expanded=True):
        st.write(f"**{st.session_state.get('email', '')}**")

        if st.button("🚪 ログアウト"):
            logout()
            st.rerun()

    # ============================
    # お問い合わせ
    # ============================
    with st.sidebar.expander("📩 お問い合わせ"):
        st.markdown("""
不具合や質問がある場合は
✉ barusa0517@gmail.com
""")

    # ============================
    # 開発者情報
    # ============================
    with st.sidebar.expander("🛠 開発者情報"):
        st.markdown("""
医療面接 AI シミュレーター

🏥 CATOの医療面接評価基準に基づく
医学部OSCE対策ツール
""")

    st.sidebar.caption("Version 1.0")

    return mode, scenario, subscenario, selected
