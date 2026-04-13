# 📝 小红书风格引擎 XHS Style Engine

AI写小红书文案，通过个人风格蒸馏去掉AI味。

## 核心逻辑

```
风格问卷（15题） → 风格Skill蒸馏 → 用你的风格写文案 → 去AI味后处理
```

**不是又一个AI写作套壳工具。** 核心差异：先通过结构化问卷 + 用户语料样本蒸馏出你的「个人风格Skill」，再用这个Skill约束AI输出，最后经过去AI味后处理引擎清除AI高频词和句式。

## 功能

- 🎯 **风格问卷**：15道精心设计的问题（含AB对比选择），3分钟建立你的风格档案
- 🧬 **风格蒸馏**：将问卷答案 + 写作样本转化为结构化的「风格Skill」
- ✍️ **文案生成**：输入主题，一键生成带标题、正文、标签的小红书笔记
- 🧹 **去AI味引擎**：自动替换30+个AI高频词，正则清除AI句式模式
- 📋 **一键复制**：生成结果直接复制到小红书

## 快速开始

```bash
git clone https://github.com/Yinmu/xhs-style-engine.git
cd xhs-style-engine
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env，填入你的LLM API Key
python run.py
```

打开 http://localhost:5000

## API配置

支持任何OpenAI兼容接口。推荐：

| 提供商 | BASE_URL | MODEL | 备注 |
|--------|----------|-------|------|
| 通义千问 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `qwen-plus` | 国内合规，便宜 |
| Kimi | `https://api.moonshot.cn/v1` | `moonshot-v1-8k` | 中文好，长上下文 |
| DeepSeek | `https://api.deepseek.com/v1` | `deepseek-chat` | 性价比高 |
| OpenAI | `https://api.openai.com/v1` | `gpt-4o-mini` | 效果好，需翻墙 |

## 项目结构

```
xhs-style-engine/
├── run.py                  # 启动入口
├── app/
│   ├── questionnaire.py    # 风格问卷定义（15题）
│   ├── style_distiller.py  # 风格Skill蒸馏引擎
│   ├── generator.py        # 文案生成 + 去AI味后处理
│   └── web.py              # Flask Web应用
├── templates/
│   └── index.html          # 前端单页应用
├── data/                   # 用户风格Skill存储（自动创建）
├── requirements.txt
└── .env.example
```

## 技术方案

- **风格蒸馏**：问卷答案 + 用户语料 → LLM分析 → 结构化JSON风格Skill
- **文案生成**：风格Skill注入system prompt → LLM生成 → 去AI味后处理
- **去AI味**：30+词汇替换 + 6条正则模式清除 + 格式清理
- **无需微调**：纯prompt engineering + RAG思路，零训练成本

## License

MIT
