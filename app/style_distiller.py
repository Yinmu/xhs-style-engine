"""
小红书风格引擎 - 风格Skill蒸馏器
将问卷答案 + 用户语料 → 结构化的个人风格Skill
"""

import json
from openai import OpenAI

DISTILL_SYSTEM_PROMPT = """你是一个专业的写作风格分析师。你的任务是根据用户的问卷答案和写作样本，
生成一份精确的「个人写作风格Skill」。

这个Skill将被用来指导AI以该用户的个人风格撰写小红书文案。

输出必须是以下JSON格式（用中文填写）：

{
  "persona": {
    "identity": "用户身份描述",
    "niche": ["领域1", "领域2"],
    "personality_tags": ["标签1", "标签2", "标签3"]
  },
  "voice": {
    "tone": "整体语调描述（一句话）",
    "sentence_style": "句式特征描述",
    "vocabulary_level": "用词水平描述",
    "humor_style": "幽默风格描述",
    "catchphrases": ["口头禅1", "口头禅2"],
    "emoji_pattern": "emoji使用模式描述",
    "paragraph_style": "段落组织方式"
  },
  "writing_rules": {
    "do": ["应该做的1", "应该做的2", "应该做的3", "应该做的4", "应该做的5"],
    "dont": ["不要做的1", "不要做的2", "不要做的3", "不要做的4", "不要做的5"]
  },
  "xhs_format": {
    "title_style": "标题风格描述",
    "opening_style": "开头风格描述",
    "ending_style": "结尾风格描述",
    "structure_preference": "结构偏好描述"
  },
  "sample_phrases": ["这个用户会说的典型句子1", "典型句子2", "典型句子3"]
}

注意：
1. 所有描述必须具体、可操作，不要泛泛而谈
2. 如果用户提供了写作样本，重点从样本中提取真实的语言特征
3. writing_rules的dont列表要根据用户选择的"讨厌的写作方式"来生成
4. sample_phrases要模仿用户的真实语气，不是通用句子"""


def build_distill_prompt(answers: dict) -> str:
    """将问卷答案组装成蒸馏提示词"""
    parts = ["以下是用户的写作风格问卷答案：\n"]

    label_maps = {
        "identity": {
            "student": "学生/大学生", "office": "职场打工人",
            "freelancer": "自由职业/独立创业", "mom": "全职妈妈/宝妈",
            "business": "小商家/品牌主", "other": "其他",
        },
        "persona": {
            "professional": "专业靠谱", "warm": "温暖亲切",
            "funny": "搞笑幽默", "literary": "文艺小清新",
            "grounded": "接地气真实", "energetic": "元气满满",
            "chill": "佛系淡然", "sharp": "犀利毒舌",
        },
        "niche": {
            "beauty": "美妆护肤", "fashion": "穿搭时尚",
            "food": "美食探店", "travel": "旅行出游",
            "career": "职场成长", "parenting": "母婴育儿",
            "fitness": "健身减脂", "tech": "数码科技",
            "home": "家居好物", "study": "学习干货",
            "emotion": "情感生活", "business_content": "创业/副业",
        },
        "anti_style": {
            "too_formal": "太正式/像写论文", "too_hyper": "太夸张/全是感叹号",
            "too_template": "太模板化", "too_long": "太啰嗦",
            "too_cold": "太冷淡", "too_salesy": "太营销/广告味",
            "too_emoji": "emoji太多", "too_plain": "太平淡",
        },
    }

    if v := answers.get("identity"):
        parts.append(f"【身份】{label_maps['identity'].get(v, v)}")

    if v := answers.get("niche"):
        labels = [label_maps['niche'].get(x, x) for x in v] if isinstance(v, list) else [v]
        parts.append(f"【领域】{', '.join(labels)}")

    if v := answers.get("persona"):
        labels = [label_maps['persona'].get(x, x) for x in v] if isinstance(v, list) else [v]
        parts.append(f"【期望人设】{', '.join(labels)}")

    if v := answers.get("style_ab"):
        parts.append(f"【风格偏好AB测试】选择了: {v}")

    if v := answers.get("anti_style"):
        labels = [label_maps['anti_style'].get(x, x) for x in v] if isinstance(v, list) else [v]
        parts.append(f"【讨厌的风格】{', '.join(labels)}")

    if v := answers.get("opening_style"):
        parts.append(f"【开头偏好】{v}")

    emoji_map = {"heavy": "密集型", "moderate": "适中型", "minimal": "极简型"}
    if v := answers.get("emoji_density"):
        parts.append(f"【emoji密度】{emoji_map.get(v, v)}")

    sentence_map = {"short": "短句为主", "mixed": "长短混合", "long": "偏长句"}
    if v := answers.get("sentence_style"):
        parts.append(f"【句式风格】{sentence_map.get(v, v)}")

    humor_map = {"high": "经常幽默", "medium": "偶尔幽默", "low": "基本不搞笑"}
    if v := answers.get("humor_level"):
        parts.append(f"【幽默程度】{humor_map.get(v, v)}")

    if v := answers.get("catchphrase"):
        parts.append(f"【口头禅/语气词】{v}")

    para_map = {"list": "分点列举", "story": "故事叙述", "mixed_para": "混合型"}
    if v := answers.get("paragraph_style"):
        parts.append(f"【段落风格】{para_map.get(v, v)}")

    ending_map = {
        "cta": "互动引导", "summary": "总结金句",
        "casual": "随意收尾", "cliffhanger": "留悬念",
    }
    if v := answers.get("ending_style"):
        parts.append(f"【结尾风格】{ending_map.get(v, v)}")

    formality_map = {"colloquial": "口语化", "semi_formal": "半正式", "formal": "偏正式"}
    if v := answers.get("formality"):
        parts.append(f"【用词偏好】{formality_map.get(v, v)}")

    if v := answers.get("reference_blogger"):
        parts.append(f"【参考博主】{v}")

    if v := answers.get("sample_text"):
        parts.append(f"\n【用户写作样本（重点分析）】\n{v}")

    return "\n".join(parts)


def distill_style_skill(answers: dict, client: OpenAI, model: str) -> dict:
    """核心函数：将问卷答案蒸馏为风格Skill"""
    user_prompt = build_distill_prompt(answers)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": DISTILL_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content
    skill = json.loads(raw)
    return skill
