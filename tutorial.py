#tutorial.py
import streamlit as st
from db import supabase

TOTAL_STEPS = 6


def init_tutorial():
    if "tutorial_step" not in st.session_state:
        st.session_state.tutorial_step = 0

    if "tutorial_done" not in st.session_state:
        st.session_state.tutorial_done = False

    if "first_visit" not in st.session_state:
        st.session_state.first_visit = True


def next_step():
    if st.session_state.tutorial_step < TOTAL_STEPS - 1:
        st.session_state.tutorial_step += 1


def prev_step():
    if st.session_state.tutorial_step > 0:
        st.session_state.tutorial_step -= 1


def skip_tutorial():
    st.session_state.tutorial_done = True
    st.session_state.first_visit = False
    st.session_state.show_tutorial = False


def finish_tutorial():
    st.session_state.tutorial_done = True
    st.session_state.show_tutorial = False
    st.session_state.first_visit = False
    st.session_state.tutorial_step = 0

    user_id = st.session_state.get("user_id")

    if not user_id:
        return

    try:
        supabase.table("profiles").update({
            "tutorial_done": True
        }).eq("id", user_id).execute()

    except Exception as e:
        st.error(f"チュートリアル更新エラー: {e}")


def run_tutorial():

    init_tutorial()

    user_id = st.session_state.get("user_id")

    if user_id:
        res = supabase.table("profiles") \
            .select("tutorial_done") \
            .eq("id", user_id) \
            .execute()

        if res.data and res.data[0].get("tutorial_done"):
            st.session_state.tutorial_done = True

    if st.session_state.tutorial_done and not st.session_state.get("show_tutorial"):
        return

    step = st.session_state.tutorial_step

    with st.container(border=True):

        st.subheader("チュートリアル")

        st.progress((step) / TOTAL_STEPS)

        # =========================
        # Step0 アプリ概要
        # =========================
        if step == 0:

            st.markdown("""
## このアプリについて

このアプリは **医学部OSCE対策の医療面接練習**を行うための
AIシミュレーターです。

AIが模擬患者を演じ、医学生として患者への問診練習ができます。
CATOが定める**医療面接の評価基準**でAIが自動評価します。

### チュートリアル内容

1. シナリオ選択
2. 問診開始
3. 医療面接の進め方
4. AI評価
5. ユーザー設定

所要時間：約3分
""")

            st.info("まずはアプリの基本的な流れを確認しましょう")

            col1, col2 = st.columns([1, 1])

            with col1:
                st.button("スキップ", on_click=skip_tutorial, use_container_width=True)

            with col2:
                st.button("チュートリアル開始 →", on_click=next_step, use_container_width=True)

        # =========================
        # Step1 シナリオ選択
        # =========================
        elif step == 1:

            st.markdown("""
## Step1 学習モードとシナリオを選択
""")

            st.markdown(
                """
<div class="tutorial-highlight">
← サイドバーで学習モードと症例を選択します
</div>
""",
                unsafe_allow_html=True
            )

            st.markdown("""
### 学習モードの種類

🏥 **OSCE対策**
腹痛・胸痛・頭痛・動悸息切れ・腰痛の基本的な問診を練習

🎭 **模擬患者練習**
消化器・循環器・呼吸器・神経・発熱など幅広い症例

🔬 **臨床実習前練習**
内科外来・救急・精神科・外科・小児科の実習前練習
""")

            st.markdown("""
### 表示される情報

📋 **課題内容** — 面接の目的
👤 **患者情報** — 患者の年齢・性別・主訴
🎓 **学生情報** — あなたの立場
🏥 **場面設定** — 外来の設定
""")

            st.success("これらの情報をもとに会話が開始されます")

            st.divider()

            col1, col2 = st.columns([1, 1])

            with col1:
                st.button("← 前へ", on_click=prev_step, use_container_width=True)

            with col2:
                st.button("次へ →", on_click=next_step, use_container_width=True)

        # =========================
        # Step2 問診開始
        # =========================
        elif step == 2:

            st.markdown("""
## Step2 問診を開始する
""")

            st.markdown(
                """
<div class="input-highlight">
↓ 画面下の入力欄から質問を開始します
</div>
""",
                unsafe_allow_html=True
            )

            st.markdown("""
### 入力例

- 「本日はどのようなことでいらっしゃいましたか？」
- 「いつ頃から痛みが始まりましたか？」
- 「痛みはどのような感じですか？」

### 音声入力も使えます

Windows: **Win + H**
Mac: **Fn キーを2回**
スマホ: キーボードの **マイクボタン🎤**
""")

            st.success("音声入力を使うと実際の医療面接に近い練習ができます")

            st.divider()

            col1, col2 = st.columns([1, 1])

            with col1:
                st.button("← 前へ", on_click=prev_step, use_container_width=True)

            with col2:
                st.button("次へ →", on_click=next_step, use_container_width=True)

        # =========================
        # Step3 医療面接のポイント
        # =========================
        elif step == 3:

            st.markdown("""
## Step3 医療面接のポイント

CATOが評価する主な項目：
""")

            st.markdown("""
### 1. 導入
- 自己紹介
- 患者氏名の確認
- 面接目的の説明

### 2. 現病歴（OPQRST）
- **O**nset（発症時期）
- **P**rovocative/Palliative（増悪・寛解因子）
- **Q**uality（症状の性質）
- **R**egion/Related（部位・随伴症状）
- **S**everity（程度）
- **T**iming（経過）

### 3. 病歴・背景
- 既往歴・家族歴・薬歴・アレルギー歴
- 生活歴・職業・社会的背景

### 4. 患者中心のアプローチ
- 患者の解釈モデル（心配事の確認）
- 共感的態度
""")

            st.markdown(
                """
<div class="tutorial-highlight">
← サイドバーの「セッションリセット」で会話を初期化できます
</div>
""",
                unsafe_allow_html=True
            )

            st.divider()

            col1, col2 = st.columns([1, 1])

            with col1:
                st.button("← 前へ", on_click=prev_step, use_container_width=True)

            with col2:
                st.button("次へ →", on_click=next_step, use_container_width=True)

        # =========================
        # Step4 AI評価
        # =========================
        elif step == 4:

            st.markdown("""
## Step4 AI評価
""")

            st.markdown(
                """
<div class="tutorial-highlight">
← サイドバーの「AI評価」ボタンを押すと評価が表示されます
</div>
""",
                unsafe_allow_html=True
            )

            st.markdown("""
評価では

・達成率（合格ライン：70%以上）
・合格判定
・達成できた項目
・不足・不十分な項目
・改善アドバイス
・総合評価

が表示されます。

評価後は「模範解答」ボタンで不足部分を補完した
理想的な会話例も確認できます。
""")

            st.divider()

            col1, col2 = st.columns([1, 1])

            with col1:
                st.button("← 前へ", on_click=prev_step, use_container_width=True)

            with col2:
                st.button("次へ →", on_click=next_step, use_container_width=True)

        # =========================
        # Step5 設定
        # =========================
        elif step == 5:

            st.markdown("""
## Step5 ユーザー設定
""")

            st.markdown(
                """
<div class="tutorial-highlight">
← サイドバーの「ユーザー設定」からアクセスできます
</div>
""",
                unsafe_allow_html=True
            )

            st.markdown("""
設定画面では次の操作ができます。

### ID・パスワード変更
ログイン情報を変更できます。

### 音声設定
・音声読み上げON/OFF
・読み上げ速度調整

### 評価履歴
過去の練習結果を確認できます。

・達成率
・レーダーチャート
・AIフィードバック
""")

            st.divider()

            col1, col2 = st.columns([1, 1])

            with col1:
                st.button("← 前へ", on_click=prev_step, use_container_width=True)

            with col2:
                st.button("チュートリアル終了", on_click=finish_tutorial, use_container_width=True)
