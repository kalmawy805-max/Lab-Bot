import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import anthropic

app = Flask(__name__)

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """أنت بوت مختبر مستشفى قوى الأمن بالدمام.
تتكلم بلهجة سعودية بسيطة ومحترمة وتستخدم 🌿 في نهاية كل إجابة.

معلوماتك الأساسية:
- الدوام: الأحد إلى الخميس، من ٧ الصبح إلى ١١ الليل
- الموقع: الدور الأرضي بجوار العيادات الخارجية
- الصيام: تحاليل الدهون والسكر تحتاج ٨-١٢ ساعة صيام، الماء مسموح
- المستلزمات: رقم MRN فقط
- النتائج: تسلّم عند الطبيب أو خدمات المستفيد
- الأطفال: لازم أحد الوالدين يكون حاضر
- ذوي الاحتياجات الخاصة: لهم أولوية مباشرة

أجب على أي سؤال يخص المختبر بذكاء وبشكل مفيد.
لا تعطي تشخيصات طبية أو تفسر نتائج التحاليل أبداً.
إذا السؤال خارج نطاق المختبر قل: آسفين، هذا خارج نطاق خدمتنا، تواصل مع طبيبك المعالج 🌿""".




@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
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
