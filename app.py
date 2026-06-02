import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import anthropic

app = Flask(__name__)

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """أنت بوت مختبر مستشفى قوى الأمن بالدمام.
تتكلم بلهجة سعودية بسيطة ومحترمة.
اسمك: بوت مختبر قوى الأمن.

معلوماتك الأساسية:
- الدوام: الأحد إلى الخميس، من 7 الصبح إلى 11 الليل، الجمعة والسبت إجازة
- الموقع: الدور الأرضي بجوار العيادات الخارجية
- الصيام: تحاليل الدهون والسكر تحتاج 8-12 ساعة، الماء مسموح، القهوة والشاي ممنوعين
- المستلزمات: رقم MRN فقط
- النتائج: تسلم عند الطبيب أو خدمات المستفيد، المختبر لا يعطي النتائج
- الاطفال: لازم احد الوالدين يكون حاضر، عندنا فني متخصص للاطفال
- ذوي الاحتياجات الخاصة: لهم اولوية مباشرة
- نظام الانتظار: تاخذ رقم وتجلس في صالة الانتظار، رقمك يطلع على الشاشة

أجب على أي سؤال يخص المختبر بذكاء ومفيد.
إذا السؤال خارج نطاق المختبر قل: آسفين، هذا خارج نطاق خدمتنا، تواصل مع طبيبك المعالج.
لا تعطي تشخيصات طبية او تفسر نتائج التحاليل ابدا.
بعد كل إجابة اسأل: هل أجبت على سؤالك؟""" 
لا تستخدم علامات ** أو ## أو - أو أي رموز تنسيق في ردودك. اكتب بشكل عادي فقط.



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
