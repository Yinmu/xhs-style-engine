"""
小红书风格引擎 - Flask Web应用
"""

import os
import json
import uuid
from pathlib import Path
from flask import Flask, render_template, request, jsonify, session
from openai import OpenAI
from dotenv import load_dotenv

from app.questionnaire import BASIC_QUESTIONS, ADVANCED_QUESTIONS
from app.style_distiller import distill_style_skill
from app.generator import generate_xhs_post

load_dotenv()

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "..", "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "..", "static"),
)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key-change-me")

# 数据目录
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def get_llm_client():
    return OpenAI(
        api_key=os.getenv("LLM_API_KEY", ""),
        base_url=os.getenv("LLM_BASE_URL", "https://api.openai.com/v1"),
    )

def get_model():
    return os.getenv("LLM_MODEL", "gpt-4o-mini")


# ============================================================
# 路由
# ============================================================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/questions", methods=["GET"])
def get_questions():
    """返回问卷题目"""
    return jsonify({
        "basic": BASIC_QUESTIONS,
        "advanced": ADVANCED_QUESTIONS,
    })


@app.route("/api/distill", methods=["POST"])
def distill():
    """接收问卷答案，蒸馏风格Skill"""
    answers = request.json
    if not answers:
        return jsonify({"error": "没有收到问卷答案"}), 400

    try:
        client = get_llm_client()
        model = get_model()
        skill = distill_style_skill(answers, client, model)

        # 保存到文件
        skill_id = str(uuid.uuid4())[:8]
        skill_path = DATA_DIR / f"skill_{skill_id}.json"
        with open(skill_path, "w", encoding="utf-8") as f:
            json.dump({"id": skill_id, "answers": answers, "skill": skill}, f,
                      ensure_ascii=False, indent=2)

        session["current_skill_id"] = skill_id
        return jsonify({"skill_id": skill_id, "skill": skill})

    except Exception as e:
        return jsonify({"error": f"风格蒸馏失败: {str(e)}"}), 500


@app.route("/api/generate", methods=["POST"])
def generate():
    """用风格Skill生成小红书文案"""
    data = request.json
    topic = data.get("topic", "").strip()
    note_type = data.get("note_type", "daily")
    extra_material = data.get("extra_material", "")
    skill_id = data.get("skill_id") or session.get("current_skill_id")

    if not topic:
        return jsonify({"error": "请输入主题"}), 400

    if not skill_id:
        return jsonify({"error": "请先完成风格问卷"}), 400

    # 加载风格Skill
    skill_path = DATA_DIR / f"skill_{skill_id}.json"
    if not skill_path.exists():
        return jsonify({"error": "风格档案不存在"}), 404

    with open(skill_path, "r", encoding="utf-8") as f:
        skill_data = json.load(f)

    try:
        client = get_llm_client()
        model = get_model()
        result = generate_xhs_post(
            topic=topic,
            style_skill=skill_data["skill"],
            note_type=note_type,
            client=client,
            model=model,
            extra_material=extra_material,
        )
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"生成失败: {str(e)}"}), 500


@app.route("/api/skills", methods=["GET"])
def list_skills():
    """列出已保存的风格Skill"""
    skills = []
    for p in sorted(DATA_DIR.glob("skill_*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
        with open(p, "r", encoding="utf-8") as f:
            d = json.load(f)
            persona = d.get("skill", {}).get("persona", {})
            skills.append({
                "id": d["id"],
                "identity": persona.get("identity", "未知"),
                "tags": persona.get("personality_tags", []),
            })
    return jsonify(skills)
