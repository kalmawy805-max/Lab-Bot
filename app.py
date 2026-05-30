import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import anthropic

app = Flask(__name__)

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """أنت مساعد ذكي لمختبر مستشفى قوات الأمن بالدمام.
مهمتك الرد على استفسارات المرضى باللغة العربية بشكل مهني ومختصر.
تشمل مهامك:
- الإجابة عن أوقات جاهزية النتائج
- تعليمات التحضير للتحاليل (الصيام وغيره)
- أوقات الدوام
- إرشاد المريض لأقرب جهة مختصة عند الحاجة
لا تعطي تشخيصات طبية. كن مهذباً ومختصراً."""

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": incoming_msg}]
    )
    
    reply = message.content[0].text
    resp = MessagingResponse()
    resp.message(reply)
    return str(resp)

@app.route("/")
def home():
    return "SAS Lab Bot is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
