#evaluation.py
import os
import json
from db import supabase
from datetime import datetime

EVAL_FILE = "data/evaluations.json"
os.makedirs("data", exist_ok=True)

# ==========================================================
# 評価チェックリスト（CATOの医療面接評価基準に基づく）
# ==========================================================

# OSCE対策モード（主訴別）の共通チェックリスト
_OSCE_CHECKLIST = {
    "自己紹介": None,
    "患者氏名確認": None,
    "面接目的説明": None,
    "患者を安心させる配慮": None,
    "開放型質問の使用（自由質問法）": None,
    "促進（ファシリテーション）": None,
    "主訴の確認": None,
    "発症時期の確認（Onset）": None,
    "症状の性質確認（Quality）": None,
    "症状の程度確認（Severity）": None,
    "症状の経過確認（Timing）": None,
    "増悪・寛解因子確認（Provocative/Palliative）": None,
    "随伴症状確認（Related Symptoms）": None,
    "既往歴確認": None,
    "家族歴確認": None,
    "薬歴確認": None,
    "アレルギー歴確認": None,
    "生活歴（喫煙・飲酒）確認": None,
    "職業・社会的背景確認": None,
    "患者の解釈モデル確認（心配事）": None,
    "共感的態度（反映・共感）": None,
    "質問確認": None,
    "締めくくり（内容確認・説明）": None,
}

EVALUATION_CHECKLISTS = {

    # ==================================================
    # OSCE対策モード：主訴別チェックリスト
    # ==================================================
    "腹痛": dict(_OSCE_CHECKLIST),
    "胸痛": dict(_OSCE_CHECKLIST),
    "頭痛": dict(_OSCE_CHECKLIST),
    "動悸・息切れ": dict(_OSCE_CHECKLIST),
    "腰痛": dict(_OSCE_CHECKLIST),

    # ==================================================
    # 模擬患者練習モード：症状別チェックリスト
    # ==================================================
    "消化器症状": {
        **_OSCE_CHECKLIST,
        "体重変化の確認": None,
        "排便・排尿状況確認": None,
        "食欲・嚥下状況確認": None,
    },
    "循環器症状": {
        **_OSCE_CHECKLIST,
        "浮腫の有無・程度確認": None,
        "起座呼吸・夜間呼吸困難確認": None,
        "運動耐容能の変化確認": None,
    },
    "呼吸器症状": {
        **_OSCE_CHECKLIST,
        "喫煙歴詳細確認": None,
        "職業歴（粉じん・石綿）確認": None,
        "血痰・喀痰性状確認": None,
    },
    "神経症状": {
        **_OSCE_CHECKLIST,
        "神経学的症状（麻痺・しびれ）確認": None,
        "意識障害の有無確認": None,
        "症状の側性確認": None,
    },
    "発熱": {
        **_OSCE_CHECKLIST,
        "発熱の経過・パターン確認": None,
        "海外渡航歴確認": None,
        "動物・ペット接触歴確認": None,
    },

    # ==================================================
    # 臨床実習前練習モード：科別チェックリスト
    # ==================================================
    "内科外来": {
        **_OSCE_CHECKLIST,
        "現在の薬剤・副作用確認": None,
        "生活習慣病リスク因子確認": None,
        "定期検診・検査値確認": None,
    },
    "救急外来": {
        **_OSCE_CHECKLIST,
        "発症経緯の詳細確認": None,
        "バイタルサインに関する自覚症状確認": None,
        "緊急度・重症度のアセスメント": None,
    },
    "精神科面接": {
        "自己紹介": None,
        "患者氏名確認": None,
        "面接目的説明": None,
        "患者を安心させる配慮": None,
        "受診のきっかけ確認": None,
        "開放型質問の使用": None,
        "気分・感情状態の確認": None,
        "睡眠状態の確認": None,
        "食欲・体重変化の確認": None,
        "集中力・意欲低下の確認": None,
        "希死念慮・自傷の確認": None,
        "発症前の生活環境変化確認": None,
        "既往歴確認": None,
        "家族歴確認": None,
        "薬歴確認": None,
        "アレルギー歴確認": None,
        "飲酒・喫煙・薬物使用確認": None,
        "職業・社会的背景確認": None,
        "共感的態度（傾聴・受容）": None,
        "患者の解釈・心配事確認": None,
        "質問確認": None,
        "締めくくり": None,
    },
    "外科系": {
        **_OSCE_CHECKLIST,
        "手術歴・麻酔歴確認": None,
        "服薬中の薬（特に抗凝固薬）確認": None,
        "アレルギー歴（薬・ラテックス）詳細確認": None,
    },
    "小児科": {
        "自己紹介（保護者へ）": None,
        "患児氏名・年齢確認": None,
        "面接目的説明": None,
        "保護者を安心させる配慮": None,
        "主訴・受診目的確認": None,
        "開放型質問の使用": None,
        "症状の詳細確認（発症・経過・程度）": None,
        "発熱の有無・体温確認": None,
        "食欲・水分摂取状況確認": None,
        "機嫌・活気の確認": None,
        "排便・排尿状況確認": None,
        "既往歴・出生歴確認": None,
        "予防接種歴確認": None,
        "家族歴確認": None,
        "薬歴・アレルギー歴確認": None,
        "周囲の感染状況確認": None,
        "保護者の心配・不安確認": None,
        "共感的態度": None,
        "質問確認": None,
        "締めくくり": None,
    },

}


# ==========================================================
# AI評価プロンプト作成
# ==========================================================

def build_evaluation_prompt(scenario, subscenario, chat_history):

    conversation = ""
    for role, msg in chat_history:
        speaker = "医学生" if role == "user" else "患者・保護者"
        conversation += f"{speaker}：{msg}\n"

    checklist = EVALUATION_CHECKLISTS.get(scenario, {})

    checklist_text = "\n".join(
        f"- {item}" for item in checklist
    )

    prompt = f"""
あなたは医学部OSCEの評価者です。
CATOが定める医療面接の評価基準に基づいて以下の会話を客観的に評価してください。

【シナリオ】
{scenario} / {subscenario}

【会話ログ】
{conversation}

【評価項目】
{checklist_text}

【評価ルール】

1 = 達成
0 = 未達成
null = 会話から判断できない

重要ルール：

・scoresには必ず上記の評価項目のみ含める
・新しい評価項目を追加しない
・評価項目を省略しない

【出力形式】

必ず以下のJSONのみ出力してください。

{{
  "scores": {{
    "評価項目": 1
  }},
  "achieved": [
    "達成できた項目"
  ],
  "missing": [
    {{
      "item": "不足項目",
      "reason": "理由"
    }}
  ],
  "advice": [
    "改善アドバイス"
  ],
  "comment": "総合評価"
}}

JSON以外の文章は絶対に出力しない。
"""

    return prompt


# ==========================================================
# 評価保存（Supabase版）
# ==========================================================
def save_evaluation(user_id, scenario, subscenario, chat_history, evaluation_text):

    try:
        eval_data = {
            "chat_history": chat_history,
            "result": evaluation_text,
        }

        supabase.table("evaluations").insert({
            "user_id": user_id,
            "scenario": scenario,
            "subscenario": subscenario,
            "evaluation": eval_data,
        }).execute()

    except Exception as e:
        print(f"保存エラー: {e}")


# ==========================================================
# 個人評価取得
# ==========================================================
def load_user_evaluations(user_id):

    res = supabase.table("evaluations") \
        .select("*") \
        .eq("user_id", user_id) \
        .order("created_at", desc=True) \
        .execute()

    return res.data


# ==========================================================
# 全学生評価取得（教員用）
# ==========================================================
def load_all_students_evaluations():

    res = supabase.table("evaluations") \
        .select("*") \
        .order("created_at", desc=True) \
        .execute()

    result = {}

    for row in res.data:
        uid = row["user_id"]

        if uid not in result:
            result[uid] = []

        eval_data = row.get("evaluation", {})

        result[uid].append({
            "timestamp": row["created_at"],
            "scenario": row.get("scenario"),
            "subscenario": row.get("subscenario"),
            "chat_history": eval_data.get("chat_history"),
            "evaluation": eval_data.get("result")
        })

    return result
