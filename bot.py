import os
import sqlite3
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import google.generativeai as genai

# التوكنات مباشرة
TELEGRAM_BOT_TOKEN = "8605350892:AAEQARoXq3LJHuQULCqeHhRQqFj6DeutxKM"
GEMINI_API_KEY = "AQ.Ab8RN6IfYfHL4I0FxGNrIH4tvdEXhRvE9oxmrP18HaaV-NBE7A"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# إعداد جيمني بالطريقة الكلاسيكية المستقرة
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    ai_model = genai.GenerativeModel("gemini-1.5-flash")
else:
    ai_model = None

def init_db():
    conn = sqlite3.connect("geomatics_bot.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            trials_left INTEGER DEFAULT 2,
            is_vip INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

init_db()

def get_or_create_user(user_id, username):
    conn = sqlite3.connect("geomatics_bot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT trials_left, is_vip FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    if not user:
        cursor.execute("INSERT INTO users (user_id, username, trials_left, is_vip) VALUES (?, ?, 2, 0)", (user_id, username))
        conn.commit()
        user = (2, 0)
    conn.close()
    return user

def update_trials(user_id):
    conn = sqlite3.connect("geomatics_bot.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET trials_left = trials_left - 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def main_menu_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("📡 أقسام الأجهزة المساحية والمعايرة", callback_data="survey_devices"))
    keyboard.row(InlineKeyboardButton("🌍 قسم الاستشعار عن بعد (ENVI & ERDAS)", callback_data="remote_sensing"))
    keyboard.row(InlineKeyboardButton("💻 برامج الـ GIS وتطبيقات البايثون", callback_data="gis_software"))
    keyboard.row(InlineKeyboardButton("🛣️ تصميم الطرق برنامج AutoCAD Civil 3D", callback_data="civil_roads"))
    keyboard.row(InlineKeyboardButton("📦 مستودع البرامج والتحميلات (Software Hub)", callback_data="software_hub"))
    keyboard.row(InlineKeyboardButton("🎓 ركن الماجستير والأبحاث الأكاديمية", callback_data="master_corner"))
    keyboard.row(InlineKeyboardButton("🛠️ أدوات المطورين وسكربتات الأتمتة", callback_data="dev_tools"))
    keyboard.row(InlineKeyboardButton("💎 باقات الاشتراك الاحترافية (VIP 1 : VIP 5)", callback_data="vip_plans"))
    keyboard.row(InlineKeyboardButton("💳 الدعم الفني وفودافون كاش", callback_data="support"))
    return keyboard

def back_to_main_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("⬅️ العودة إلى القائمة الرئيسية", callback_data="main_menu"))
    return keyboard

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    trials, is_vip = get_or_create_user(user_id, username)
    
    welcome_text = (
        f"🌐 **مرحباً بك يا {username} في المنصة الهندسية المتكاملة (Geomatics Copilot)**\n\n"
        f"✨ لديك **({trials})** تجارب مجانية للاستعلام البرمجي وتحليل البيانات.\n"
        f"🤖 **ملاحظة:** نظام الذكاء الاصطناعي مفعل الآن بالكامل؛ يمكنك إرسال أي سؤال هندسي أو برمجي وسأقوم بالرد عليك فوراً!\n\n"
        f"👇 **اختر القسم المناسب لعملك من القائمة أدناه:**"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=main_menu_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    trials, is_vip = get_or_create_user(user_id, call.from_user.username)
    
    if call.data == "main_menu":
        bot.answer_callback_query(call.id)
        bot.edit_message_text("🌐 **القائمة الرئيسية للمنصة:**\nاختر أحد الأقسام أدناه:", call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=main_menu_keyboard())

    elif call.data == "survey_devices":
        bot.answer_callback_query(call.id)
        text = (
            "📡 **قسم الأجهزة المساحية والمعايرة:**\n\n"
            "• **Total Station:** شاشات التشغيل، القياسات الرصدية، وتصحيح أخطاء التوجيه.\n"
            "• **GPS / GNSS:** إعدادات الـ RTK، ربط الشبكات الجيوديسية، وتحويل الإحداثيات.\n"
            "• **Digital Level:** الموازنات الدقيقة وحساب مناسيب النقاط بدقة عالية."
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())

    elif call.data == "remote_sensing":
        bot.answer_callback_query(call.id)
        text = (
            "🌍 **قسم الاستشعار عن بعد (Remote Sensing):**\n\n"
            "• **برنامج ENVI:** معالجة الصور الفضائية المتقدمة، التحليل الطيفي، وإزالة التشويش الجوي.\n"
            "• **برنامج ERDAS Imagine:** التصحيح الهندسي للمرئيات وتصنيف الصور (Image Classification).\n"
            "• **مؤشرات الغطاء النباتي:** حساب مؤشرات مثل (NDVI, NDWI) عبر بايثون أو برامج المعالجة."
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())

    elif call.data == "gis_software":
        bot.answer_callback_query(call.id)
        text = (
            "💻 **برامج الـ GIS وتطبيقات البايثون:**\n\n"
            "• **ArcGIS Pro:** بناء قواعد البيانات الجغرافية (Geodatabases) والتحليل المكاني المتقدم.\n"
            "• **QGIS:** الخرائط الرقمية المفتوحة وتكامل الإضافات البرمجية.\n"
            "• **Python & ArcPy:** أتمتة المهام واستخراج التقارير الجغرافية آلياً."
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())

    elif call.data == "civil_roads":
        bot.answer_callback_query(call.id)
        text = (
            "🛣️ **قسم تصميم الطرق (AutoCAD Civil 3D):**\n\n"
            "• إنشاء مسارات الطرق المحورية (Alignments) والقطاعات الطولية (Profiles).\n"
            "• تصميم القطاعات العرضية (Assemblies & Corridors).\n"
            "• حساب كميات الحفر والردم (Earthwork Quantities & Cut/Fill Tables)."
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())

    elif call.data == "software_hub":
        bot.answer_callback_query(call.id)
        text = (
            "📦 **مستودع البرامج المتاحة (Software Hub):**\n\n"
            "إليك روابط تحميل أهم برامج المجال (مع الكراك والتفعيل المتاح):\n\n"
            "1. **ArcGIS Pro (Latest):** [تحميل مباشر مع التفعيل](https://example.com/arcgis)\n"
            "2. **AutoCAD Civil 3D:** [تحميل مع الكراك](https://example.com/civil3d)\n"
            "3. **ENVI & ERDAS Imagine:** [روابط النسخ والتفعيل](https://example.com/envi-erdas)\n"
            "4. **QGIS Software:** [النسخة الرسمية المجانية](https://qgis.org)\n\n"
            "*(ملاحظة: يتم تحديث الروابط بانتظام)*"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())

    elif call.data == "master_corner":
        bot.answer_callback_query(call.id)
        text = (
            "🎓 **ركن الماجستير والأبحاث الأكاديمية:**\n\n"
            "• مقترحات أبحاث رسائل الماجستير والدكتوراه في الجيوماتكس ونظم المعلومات.\n"
            "• مراجع مساحية وكتب علمية متخصصة.\n"
            "• مصادر قواعد بيانات مكانية عالمية مجانية."
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())

    elif call.data == "dev_tools":
        bot.answer_callback_query(call.id)
        if trials > 0 or is_vip:
            if not is_vip:
                update_trials(user_id)
            text = (
                f"🛠️ **أدوات المطورين وسكربتات الأتمتة:**\n"
                f"تم استهلاك تجربة. المتبقي لديك: {max(0, trials-1)} تجارب.\n\n"
                f"إليك كود بايثون سريع للتحقق من الطبقات الجغرافية:\n"
                f"```python\nimport arcpy\narcpy.env.workspace = 'C:/Data'\nfc_list = arcpy.ListFeatureClasses()\nprint(fc_list)\n```"
            )
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())
        else:
            bot.answer_callback_query(call.id, "⚠️ نفذت رصيدك المجاني، يرجى ترقية حسابك لأحد باقات VIP.", show_alert=True)

    elif call.data == "vip_plans":
        bot.answer_callback_query(call.id)
        text = (
            "💎 **تفاصيل باقات الاشتراك الاحترافية (VIP 1 إلى VIP 5):**\n\n"
            "🔹 **VIP 1 - الباقة الأساسية:** تشمل الأجهزة المساحية وأساسيات الـ GIS.\n"
            "🔹 **VIP 2 - الباقة المتقدمة:** أساسيات الـ GIS + الاستشعار عن بعد (ENVI & ERDAS).\n"
            "🔹 **VIP 3 - الباقة الاحترافية:** الاستشعار عن بعد + تصميم الطرق ببرنامج Civil 3D.\n"
            "🔹 **VIP 4 - باقة ركن الماجستير:** المراجع الأكاديمية والدعم البحثي وتحليل البيانات.\n"
            "🔹 **VIP 5 - الباقة الشاملة (All-In-One):** الوصول الكامل لكل الأقسام وبرامج المجال وأكواد البايثون."
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())

    elif call.data == "support":
        bot.answer_callback_query(call.id)
        text = (
            "💳 **الدعم الفني وفودافون كاش:**\n\n"
            "لإتمام الاشتراك، يرجى التحويل على محفظة فودافون كاش الرسمية التالية:\n"
            "📲 **رقم المحفظة:** `01012345678`\n\n"
            "ثم أرسل صورة إيصال التحويل هنا لتفعيل حسابك فوراً."
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())

@bot.message_handler(func=lambda message: True)
def handle_ai_chat(message):
    if not ai_model:
        bot.reply_to(message, "مرحباً ديفيد! النظام يعمل ولكن مفتاح الذكاء الاصطناعي بحاجة للتأكيد.")
        return
    
    try:
        prompt = f"أنت مساعد خبير ومحترف في الجيوماتكس، المساحة، نظم المعلومات الجغرافية GIS، ولغة بايثون للخرائط (ArcPy). أجب باحترافية باللغة العربية على السؤال التالي: {message.text}"
        response = ai_model.generate_content(prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"AI Error: {e}")
        bot.reply_to(message, "عذراً، حدث خطأ مؤقت أثناء معالجة طلبك عبر الذكاء الاصطناعي.")

if __name__ == "__main__":
    print("Bot is running perfectly...")
    bot.infinity_polling()
