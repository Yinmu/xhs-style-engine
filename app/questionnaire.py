"""
小红书风格引擎 - 风格问卷定义
通过结构化问题收集用户的写作风格DNA
"""

# ============================================================
# 基础层问卷（5题，1分钟完成）
# ============================================================
BASIC_QUESTIONS = [
    {
        "id": "identity",
        "question": "你是什么身份？",
        "type": "single_choice",
        "options": [
            {"value": "student", "label": "学生/大学生"},
            {"value": "office", "label": "职场打工人"},
            {"value": "freelancer", "label": "自由职业/独立创业"},
            {"value": "mom", "label": "全职妈妈/宝妈"},
            {"value": "business", "label": "小商家/品牌主"},
            {"value": "other", "label": "其他"},
        ],
    },
    {
        "id": "niche",
        "question": "你的小红书主要写什么？",
        "type": "multi_choice",
        "max_select": 3,
        "options": [
            {"value": "beauty", "label": "美妆护肤"},
            {"value": "fashion", "label": "穿搭时尚"},
            {"value": "food", "label": "美食探店"},
            {"value": "travel", "label": "旅行出游"},
            {"value": "career", "label": "职场成长"},
            {"value": "parenting", "label": "母婴育儿"},
            {"value": "fitness", "label": "健身减脂"},
            {"value": "tech", "label": "数码科技"},
            {"value": "home", "label": "家居好物"},
            {"value": "study", "label": "学习干货"},
            {"value": "emotion", "label": "情感生活"},
            {"value": "business_content", "label": "创业/副业"},
        ],
    },
    {
        "id": "persona",
        "question": "你希望读者觉得你是什么样的人？",
        "type": "multi_choice",
        "max_select": 3,
        "options": [
            {"value": "professional", "label": "专业靠谱"},
            {"value": "warm", "label": "温暖亲切"},
            {"value": "funny", "label": "搞笑幽默"},
            {"value": "literary", "label": "文艺小清新"},
            {"value": "grounded", "label": "接地气真实"},
            {"value": "energetic", "label": "元气满满"},
            {"value": "chill", "label": "佛系淡然"},
            {"value": "sharp", "label": "犀利毒舌"},
        ],
    },
    {
        "id": "style_ab",
        "question": "下面两种开头，你更像哪个？",
        "type": "ab_choice",
        "pairs": [
            {
                "a": "姐妹们！！这个面霜我真的要吹爆💥 用了一周皮肤嫩得跟剥了壳的鸡蛋一样",
                "b": "最近入手了一款面霜，用了大概一周，来跟大家分享一下真实感受",
                "a_tag": "热情奔放型",
                "b_tag": "理性克制型",
            },
            {
                "a": "救命！！谁懂啊 这家店也太好吃了吧😭😭",
                "b": "周末去了一家藏在巷子里的小店，环境一般但味道惊艳",
                "a_tag": "情绪爆发型",
                "b_tag": "娓娓道来型",
            },
            {
                "a": "打工人的早餐不需要仪式感，需要的是5分钟搞定还好吃🥲",
                "b": "分享我的快手早餐合集，每天不重样，最快3分钟出锅",
                "a_tag": "共情吐槽型",
                "b_tag": "实用教程型",
            },
        ],
    },
    {
        "id": "anti_style",
        "question": "你最讨厌的写作方式是什么？（可多选）",
        "type": "multi_choice",
        "max_select": 3,
        "options": [
            {"value": "too_formal", "label": "太正式/像写论文"},
            {"value": "too_hyper", "label": "太夸张/全是感叹号"},
            {"value": "too_template", "label": "太模板化/一看就是套路"},
            {"value": "too_long", "label": "太啰嗦/废话太多"},
            {"value": "too_cold", "label": "太冷淡/没有温度"},
            {"value": "too_salesy", "label": "太营销/广告味太重"},
            {"value": "too_emoji", "label": "emoji太多/花里胡哨"},
            {"value": "too_plain", "label": "太平淡/没有记忆点"},
        ],
    },
]

# ============================================================
# 进阶层问卷（10题，3分钟完成）
# ============================================================
ADVANCED_QUESTIONS = [
    {
        "id": "opening_style",
        "question": "选出你更喜欢的小红书开头风格",
        "type": "ab_choice",
        "pairs": [
            {
                "a": "被问了800遍的穿搭公式，今天一次说清楚👇",
                "b": "最近总有姐妹问我怎么搭配，整理了一下我的心得~",
                "a_tag": "数据钩子型",
                "b_tag": "自然引入型",
            },
            {
                "a": "我妈看到我的工资条沉默了……",
                "b": "聊聊毕业三年的真实收入变化",
                "a_tag": "悬念故事型",
                "b_tag": "直接主题型",
            },
        ],
    },
    {
        "id": "emoji_density",
        "question": "你喜欢的emoji使用密度？",
        "type": "single_choice",
        "options": [
            {"value": "heavy", "label": "密集型 ✨💕🔥 每句话都要有"},
            {"value": "moderate", "label": "适中型 偶尔点缀一下"},
            {"value": "minimal", "label": "极简型 几乎不用或只用1-2个"},
        ],
    },
    {
        "id": "sentence_style",
        "question": "你的句子风格更接近？",
        "type": "single_choice",
        "options": [
            {"value": "short", "label": "短句为主，节奏快，像说话"},
            {"value": "mixed", "label": "长短混合，有节奏感"},
            {"value": "long", "label": "偏长句，逻辑完整，信息量大"},
        ],
    },
    {
        "id": "humor_level",
        "question": "你的内容里幽默感占多少？",
        "type": "single_choice",
        "options": [
            {"value": "high", "label": "经常玩梗/自嘲/段子"},
            {"value": "medium", "label": "偶尔幽默一下"},
            {"value": "low", "label": "基本不搞笑，认真输出"},
        ],
    },
    {
        "id": "catchphrase",
        "question": "你有什么口头禅或常用语气词吗？",
        "type": "text_input",
        "placeholder": "比如：救命、绝了、真的会谢、啊啊啊、宝子们、家人们……",
        "required": False,
    },
    {
        "id": "paragraph_style",
        "question": "你喜欢的段落风格？",
        "type": "single_choice",
        "options": [
            {"value": "list", "label": "分点列举，清晰明了"},
            {"value": "story", "label": "故事叙述，娓娓道来"},
            {"value": "mixed_para", "label": "混合型，看内容决定"},
        ],
    },
    {
        "id": "ending_style",
        "question": "你通常怎么结尾？",
        "type": "single_choice",
        "options": [
            {"value": "cta", "label": "互动引导（你们觉得呢？评论区聊聊~）"},
            {"value": "summary", "label": "总结金句（一句话概括核心观点）"},
            {"value": "casual", "label": "随意收尾（就酱~下次见）"},
            {"value": "cliffhanger", "label": "留悬念（下篇告诉你们结果…）"},
        ],
    },
    {
        "id": "formality",
        "question": "你的用词偏好？",
        "type": "single_choice",
        "options": [
            {"value": "colloquial", "label": "口语化，像跟朋友聊天"},
            {"value": "semi_formal", "label": "半正式，有干货但不端着"},
            {"value": "formal", "label": "偏正式，专业感强"},
        ],
    },
    {
        "id": "sample_text",
        "question": "粘贴1-3条你写过的文字（朋友圈、聊天记录、笔记都行）",
        "type": "long_text",
        "placeholder": "粘贴你平时写的内容，AI会从中学习你的真实风格...\n\n可以是朋友圈文案、微信聊天、备忘录笔记等任何你写的文字",
        "required": False,
    },
    {
        "id": "reference_blogger",
        "question": "有没有你觉得风格最像你（或你想学的）的博主？",
        "type": "text_input",
        "placeholder": "填博主名字或小红书ID，没有可以跳过",
        "required": False,
    },
]
