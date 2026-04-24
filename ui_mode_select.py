# ui_mode_select.py
import streamlit as st

LEARNING_MODES = {
    "OSCE対策": {
        "icon": "🏥",
        "description": "医学部3〜4年生向け。OSCE試験対策として、主要な主訴（腹痛・胸痛・頭痛・動悸息切れ・腰痛）の医療面接を繰り返し練習します。CATOの評価基準に基づいてAIが評価します。",
        "color": "#10b981",
    },
    "模擬患者練習": {
        "icon": "🎭",
        "description": "標準化患者（SP）を想定したより現実的な医療面接の練習。消化器・循環器・呼吸器・神経・発熱など幅広い症状を扱い、実際の外来に近い練習ができます。",
        "color": "#3b82f6",
    },
    "臨床実習前練習": {
        "icon": "🔬",
        "description": "5〜6年生の臨床実習に向けた準備練習。内科・救急・精神科・外科など実習で遭遇する複雑な症例を想定し、高度な問診・共感的コミュニケーションを学びます。",
        "color": "#8b5cf6",
    },
}


def render_mode_select_page():
    st.markdown(
        """
        <div style="text-align: center; padding: 1rem 0 0.5rem;">
            <h2 style="font-size: 1.3rem; font-weight: 700; color: rgba(255,255,255,0.9);">
                学習モードを選択してください
            </h2>
            <p style="font-size: 0.85rem; color: rgba(255,255,255,0.5); margin-top: 0.2rem;">
                目的に合ったモードを選ぶと、シナリオと評価基準が切り替わります
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(3)

    for i, (mode_name, info) in enumerate(LEARNING_MODES.items()):
        with cols[i]:
            color = info["color"]
            st.markdown(
                f"""
                <div style="
                    background: rgba(255,255,255,0.04);
                    border: 1px solid rgba(255,255,255,0.1);
                    border-radius: 16px;
                    padding: 1.2rem 1rem;
                    min-height: 180px;
                    margin-bottom: 0.5rem;
                ">
                    <div style="font-size: 2rem; text-align: center;">{info['icon']}</div>
                    <div style="
                        font-size: 1rem;
                        font-weight: 700;
                        text-align: center;
                        color: white;
                        margin: 0.4rem 0;
                    ">{mode_name}</div>
                    <div style="
                        font-size: 0.78rem;
                        color: rgba(255,255,255,0.55);
                        line-height: 1.55;
                        text-align: center;
                    ">{info['description']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(
                f"{info['icon']} {mode_name}を始める",
                key=f"mode_{mode_name}",
                use_container_width=True,
            ):
                st.session_state["learning_mode"] = mode_name
                st.rerun()
