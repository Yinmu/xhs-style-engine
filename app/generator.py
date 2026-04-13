"""
小红书风格引擎 - 文案生成器
用风格Skill约束AI输出 + 去AI味后处理
"""

import re
import random
import json
from openai import OpenAI


# ============================================================
# 去AI味：需要替换/删除的AI高频词
# ============================================================
AI_SMELL_WORDS = {
    # AI常用的总结性词汇 → 替换为更口语化的表达
    "值得一提的是": "",
    "总的来说": "",
    "综上所述": "",
    "不得不说": "",
    "众所周知": "",
    "毋庸置疑": "",
    "事实上": "",
    "实际上": "其实",
    "需要注意的是": "注意⚠️",
    "首先": "",
    "其次": "",
    "最后": "",
    "此外": "",
    "另外": "还有",
    "因此": "所以",
    "然而": "但是",
    "尽管如此": "不过",
    "与此同时": "",
    "在这个过程中": "",
    "从某种程度上来说": "",
    "不可否认": "",
    "显而易见": "",
    "一言以蔽之": "",
    "总而言之": "",
    "由此可见": "",
    "换言之": "说白了",
    "简而言之": "简单说",
}

# AI常用的句式模式（正则）
AI_PATTERNS = [
    (r"作为一[个名位].*?[，,]", ""),  # "作为一个XX，"
    (r"在当今.*?(?:时代|社会|背景下)[，,]", ""),  # "在当今XX时代，"
    (r"随着.*?的(?:发展|普及|兴起)[，,]", ""),  # "随着XX的发展，"
    (r"(?:让我们|我们来)一起(?:看看|了解|探讨)", "来看看"),
    (r"希望(?:本文|这篇|以上).*?(?:帮助|启发)", ""),
    (r"如果你(?:也|还)有.*?(?:欢迎|可以).*?(?:分享|留言|评论)", ""),
]


def remove_ai_smell(text: str) -> str:
    """去AI味后处理"""
    # 1. 替换AI高频词
    for ai_word, replacement in AI_SMELL_WORDS.items():
        text = text.replace(ai_word, replacement)

    # 2. 正则替换AI句式
    for pattern, replacement in AI_PATTERNS:
        text = re.sub(pattern, replacement, text)

    # 3. 清理多余空行和空格
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"^[，,。.]+", "", text, flags=re.MULTILINE)
    # 清理行首多余空格
    lines = text.split("\n")
    lines = [line.strip() for line in lines]
    text = "\n".join(lines)

    return text.strip()


def build_generation_prompt(style_skill: dict) -> str:
    """将风格Skill转化为生成用的system prompt"""
    s = style_skill
    persona = s.get("persona", {})
    voice = s.get("voice", {})
    rules = s.get("writing_rules", {})
    xhs = s.get("xhs_format", {})
    samples = s.get("sample_phrases", [])

    prompt_parts = [
        "你是一个小红书文案写手。你必须严格按照以下「个人风格Skill」来写作，",
        "让输出的文案听起来像是这个真人写的，而不是AI生成的。\n",
        "═══ 个人风格Skill ═══\n",
        f"【身份】{persona.get('identity', '创作者')}",
        f"【领域】{', '.join(persona.get('niche', []))}",
        f"【人设标签】{', '.join(persona.get('personality_tags', []))}\n",
        f"【语调】{voice.get('tone', '')}",
        f"【句式】{voice.get('sentence_style', '')}",
        f"【用词水平】{voice.get('vocabulary_level', '')}",
        f"【幽默风格】{voice.get('humor_style', '')}",
        f"【口头禅】{', '.join(voice.get('catchphrases', []))}",
        f"【emoji模式】{voice.get('emoji_pattern', '')}",
        f"【段落风格】{voice.get('paragraph_style', '')}\n",
        f"【标题风格】{xhs.get('title_style', '')}",
        f"【开头风格】{xhs.get('opening_style', '')}",
        f"【结尾风格】{xhs.get('ending_style', '')}",
        f"【结构偏好】{xhs.get('structure_preference', '')}\n",
    ]

    if rules.get("do"):
        prompt_parts.append("【必须做到】")
        for item in rules["do"]:
            prompt_parts.append(f"  ✓ {item}")

    if rules.get("dont"):
        prompt_parts.append("【绝对禁止】")
        for item in rules["dont"]:
            prompt_parts.append(f"  ✗ {item}")

    if samples:
        prompt_parts.append("\n【这个人会说的话（模仿这种语气）】")
        for s in samples:
            prompt_parts.append(f"  「{s}」")

    prompt_parts.extend([
        "\n═══ 输出格式要求 ═══",
        "1. 先输出3个备选标题（每行一个，用①②③标号）",
        "2. 空一行后输出正文",
        "3. 正文末尾空一行后输出3-5个相关话题标签（#开头）",
        "4. 不要输出任何解释、说明或元信息",
        "\n═══ 去AI味铁律 ═══",
        "- 禁止使用：值得一提的是、总的来说、综上所述、不得不说、众所周知",
        "- 禁止使用：首先/其次/最后 这种教科书式排列",
        "- 禁止使用：作为一个XX、在当今XX时代、随着XX的发展",
        "- 禁止使用过于工整的排比句",
        "- 句子要有长有短，像真人说话一样有呼吸感",
        "- 可以有不完美的表达、口语化的转折、突然的感叹",
    ])

    return "\n".join(prompt_parts)


# 笔记类型对应的额外指令
NOTE_TYPE_INSTRUCTIONS = {
    "recommend": "这是一篇种草/推荐笔记。重点突出产品/地方的亮点，用真实体验感打动人，不要像广告。",
    "tutorial": "这是一篇教程/干货笔记。重点是实用性和可操作性，步骤清晰但不要太教条。",
    "daily": "这是一篇日常分享笔记。重点是真实感和共鸣，像在跟朋友聊天。",
    "review": "这是一篇测评/对比笔记。重点是客观但有态度，给出明确的个人判断。",
    "story": "这是一篇故事/经历笔记。重点是叙事节奏和情感共鸣，有起伏有细节。",
}


def generate_xhs_post(
    topic: str,
    style_skill: dict,
    note_type: str,
    client: OpenAI,
    model: str,
    extra_material: str = "",
) -> dict:
    """
    生成小红书文案
    返回 {"titles": [...], "body": "...", "tags": [...], "raw": "..."}
    """
    system_prompt = build_generation_prompt(style_skill)
    type_instruction = NOTE_TYPE_INSTRUCTIONS.get(note_type, "")

    user_parts = [f"请用我的个人风格写一篇小红书笔记。\n\n主题/关键词：{topic}"]
    if type_instruction:
        user_parts.append(f"\n笔记类型：{type_instruction}")
    if extra_material:
        user_parts.append(f"\n参考素材：\n{extra_material}")

    user_prompt = "\n".join(user_parts)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.85,
    )

    raw_output = response.choices[0].message.content
    cleaned = remove_ai_smell(raw_output)

    # 解析标题、正文、标签
    result = parse_output(cleaned)
    result["raw"] = raw_output
    return result


def parse_output(text: str) -> dict:
    """解析生成的文案，分离标题、正文、标签"""
    lines = text.strip().split("\n")
    titles = []
    body_lines = []
    tags = []
    section = "titles"

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if section == "titles" and titles:
                section = "body"
            continue

        # 标题行
        if section == "titles" and re.match(r"^[①②③④⑤\d]", stripped):
            title = re.sub(r"^[①②③④⑤\d][.、)\]：:\s]*", "", stripped)
            if title:
                titles.append(title)
            continue

        # 标签行
        if stripped.startswith("#"):
            tags.extend(re.findall(r"#\S+", stripped))
            section = "tags"
            continue

        if section == "tags" and "#" in stripped:
            tags.extend(re.findall(r"#\S+", stripped))
            continue

        if section != "tags":
            section = "body"
            body_lines.append(line)

    return {
        "titles": titles[:3] if titles else ["（标题生成中…）"],
        "body": "\n".join(body_lines).strip(),
        "tags": tags[:5],
    }
