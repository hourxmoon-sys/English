import os
from openai import OpenAI
from anthropic import Anthropic
from google import genai

# ملاحظة: يمكنك وضع المفاتيح مباشرة هنا أو في متغيرات البيئة
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

def generate_ai_response(prompt: str, provider: str = "openai") -> str:
    """توليد استجابة من مزود الذكاء الاصطناعي المختار."""
    try:
        if provider == "openai":
            client = OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content

        elif provider == "deepseek":
            client = OpenAI(
                api_key=DEEPSEEK_API_KEY,
                base_url="https://api.deepseek.com"
            )
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content

        elif provider == "claude":
            client = Anthropic(api_key=ANTHROPIC_API_KEY)
            message = client.messages.create(
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}],
                model="claude-3-5-sonnet-latest"
            )
            return message.content[0].text

        elif provider == "gemini":
            client = genai.Client(api_key=GEMINI_API_KEY)
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            return response.text

        else:
            return "الرجاء اختيار مزود ذكاء اصطناعي صالح."
    except Exception as e:
        return f"حدث خطأ في الاتصال بمزود الذكاء الاصطناعي: {str(e)}"
