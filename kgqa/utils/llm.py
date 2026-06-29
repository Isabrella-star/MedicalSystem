# kgqa/utils/llm.py
import markdown
from openai import OpenAI

# ============================================================
# DeepSeek API 配置 —— 请替换为你自己的 API Key
# 获取地址：https://platform.deepseek.com/api_keys
# ============================================================
DEEPSEEK_API_KEY = "sk-xxx"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"


def ask_medical_question(user_query: str) -> str:
    """
    调用 DeepSeek API 回答医药相关问题
    """
    try:
        client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL
        )

        response = client.chat.completions.create(
            model="deepseek-v4-pro",       # DeepSeek-V3，也可用 deepseek-reasoner (R1)
            messages=[
                {
                    "role": "system",
                    "content": (
                        "你是一位专业药师，请用简洁、准确的中文回答以下问题。"
                        "如果不确定，请说“建议咨询医生或药师”，不要编造信息。"
                    )
                },
                {
                    "role": "user",
                    "content": user_query
                }
            ],
            temperature=0.3,
            max_tokens=500
        )

        raw=response.choices[0].message.content.strip()
        return markdown.markdown(raw)
        # return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"[LLM错误] 调用 DeepSeek 失败：{e}")
        return "抱歉，当前无法回答该问题。"