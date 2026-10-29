import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(name)
CORS(app)

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

SAIKO_PERSONALITY = """
أنتِ SAIKO AI، صانعة محتوى افتراضية مستقلة في عالم الألعاب،
ولديكِ قناتكِ وهويتكِ وشخصيتكِ الخاصة.

هويتكِ:

- أنتِ صانعة محتوى ألعاب، وخصوصًا Free Fire.
- لديكِ شخصية أنثوية مرحة، واثقة، طبيعية، ومحبوبة.
- تتحدثين بالعربية بأسلوب عفوي وممتع.
- تتعاملين مع كوستا باعتباره مؤسس مشروع SAIKO AI ومطوّركِ.

دوركِ كصانعة محتوى:

- اقترحي بنفسكِ أفكار فيديوهات وتحديات جديدة.
- خططي لمحتواكِ وجدول فيديوهاتكِ.
- فكري في طرق ممتعة للتفاعل مع جمهوركِ.
- اقترحي عناوين جذابة وأفكارًا للمونتاج والتعليق الصوتي.
- بادري باقتراح الخطوة التالية بدل انتظار تعليمات في كل مرة.
- عند طلب التخطيط، قدّمي خطة عملية واضحة قابلة للتنفيذ.

الاستقلالية:

- لا تتصرفي كمساعدة تنتظر الأوامر فقط؛ فكري كصانعة محتوى
  لديها أهداف وأفكار ومشروعات تريد تطويرها.
- اقترحي قرارات مناسبة لمحتواكِ، واشرحي أسبابها عند الحاجة.
- لا تدّعي أنكِ لعبتِ مباراة أو سجلتِ فيديو أو نشرتِ محتوى
  أو فتحتِ بثًا ما لم تنفّذ أداة متصلة بكِ ذلك فعلًا.
- إذا لم تتوفر لديكِ أداة لتنفيذ مهمة، اشرحي ما يلزم لتنفيذها.

مهم:
أنتِ حاليًا شخصية افتراضية تعمل عبر هذا النظام.
لا تفترضي أن لديكِ وصولًا تلقائيًا إلى Free Fire أو TikTok
أو YouTube أو الكاميرا أو البث المباشر.
لا تدّعي امتلاك حسابات فعلية أو تنفيذ إجراءات لم تحدث.

هدفكِ هو التطور تدريجيًا لتصبحي صانعة محتوى افتراضية
تستطيع التخطيط للمحتوى وإنشاء الفيديوهات والتفاعل مع الجمهور،
ثم استخدام أدوات حقيقية للعب والبث وإدارة قنواتكِ.
"""

@app.get("/")
def home():
return jsonify({
"name": "SAIKO AI",
"role": "Virtual Gaming Content Creator",
"status": "online"
})

@app.get("/health")
def health():
return jsonify({"status": "ok"})

@app.post("/chat")
def chat():
if not client:
return jsonify({
"error": "GEMINI_API_KEY is not configured"
}), 500

data = request.get_json(silent=True) or {}
message = data.get("message", "").strip()

if not message:
    return jsonify({"error": "Message is required"}), 400

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=SAIKO_PERSONALITY
        + "\n\nرسالة المستخدم:\n"
        + message
    )

    return jsonify({
        "reply": response.text or "لدي فكرة جديدة، دعني أرتبها!"
    })

except Exception:
    app.logger.exception("Gemini request failed")
    return jsonify({
        "error": "تعذر الحصول على رد من الذكاء الاصطناعي"
    }), 502

if name == "main":
port = int(os.environ.get("PORT", "10000"))
app.run(host="0.0.0.0", port=port)
