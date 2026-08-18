import os
import sqlite3
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import google.generativeai as genai

# توكن تيليجرام مباشر ليعمل فوراً
TELEGRAM_BOT_TOKEN = "8605350892:AAEQARoXq3LJHuQULCqeHhRQqFj6DeutxKM"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

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
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("📡  أقـسـام الأجهـزة المساحيـة والمعـايـرة  📡", callback_data="survey_devices"),
        InlineKeyboardButton("🌍  قسـم الاستشـعار عـن بعـد (ENVI & ERDAS)  🌍", callback_data="remote_sensing"),
        InlineKeyboardButton("💻  بـرامـج الـ GIS وتطبيـقات البايثـون  💻", callback_data="gis_software"),
        InlineKeyboardButton("🛣️  تصميـم الطـرق بـرنامج AutoCAD Civil 3D  🛣️", callback_data="civil_roads"),
        InlineKeyboardButton("📦  مـستـودع البـرامـج والتحميـلات (Software Hub)  📦", callback_data="software_hub"),
        InlineKeyboardButton("🎓  ركـن الماجستـير والأبحـاث الأكاديميـة  🎓", callback_data="master_corner"),
        InlineKeyboardButton("🛠️  أدوات المطورين وسكربتات الأتمتة  🛠️", callback_data="dev_tools"),
        InlineKeyboardButton("💎  باقـات الاشتـراك الاحترافيـة (VIP 1 : VIP 5)  💎", callback_data="vip_plans"),
        InlineKeyboardButton("💳  الدعـم الفنـي وفودافـون كـاش  💳", callback_data="support")
    )
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
            "🔹 **VIP 1 - الباقة الأساسية:**\n"
            "• تشمل: الوصول للأجهزة المساحية وأساسيات الـ GIS.\n"
            "• (شهري: 300 EGP | ربع سنوي: 800 EGP | نصف سنوي: 1,500 EGP | سنوي: 2,800 EGP)\n\n"
            "🔹 **VIP 2 - الباقة المتقدمة:**\n"
            "• تشمل: أساسيات الـ GIS + قسم الاستشعار عن بعد (ENVI & ERDAS).\n"
            "• (شهري: 500 EGP | ربع سنوي: 1,350 EGP | نصف سنوي: 2,500 EGP | سنوي: 4,800 EGP)\n\n"
            "🔹 **VIP 3 - الباقة الاحترافية:**\n"
            "• تشمل: الاستشعار عن بعد + تصميم الطرق ببرنامج Civil 3D.\n"
            "• (شهري: 800 EGP | ربع سنوي: 2,150 EGP | نصف سنوي: 4,000 EGP | سنوي: 7,500 EGP)\n\n"
            "🔹 **VIP 4 - باقة ركن الماجستير:**\n"
            "• تشمل: المراجع الأكاديمية، الدعم البحثي، وتحليل البيانات المتقدم.\n"
            "• (شهري: 1,500 EGP | ربع سنوي: 4,050 EGP | نصف سنوي: 7,600 EGP | سنوي: 14,000 EGP)\n\n"
            "🔹 **VIP 5 - باقة أدوات المطورين الشاملة (All-In-One):**\n"
            "• تشمل: الوصول الكامل لكل الأقسام، برامج المجال والكراكات، وأكواد أتمتة البايثون بلا حدود.\n"
            "• (شهري: 2,700 EGP | ربع سنوي: 5,000 EGP | نصف سنوي: 9,500 EGP)\n"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())

    elif call.data == "support":
        bot.answer_callback_query(call.id)
        text = (
            "💳 **الدعم الفني وفودافون كاش:**\n\n"
            "لإتمام الاشتراك في أي باقة، يرجى تحويل المبلغ المستحق على محفظة فودافون كاش الرسمية التالية:\n"
            "📲 **رقم المحفظة:** `01012345678`\n\n"
            "ثم قم بإرسال **صورة إيصال التحويل** هنا في المحادثة وسيقوم النظام بتفعيل حسابك الفئة المطلوبة فوراً."
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())

@bot.message_handler(func=lambda message: True)
def handle_ai_chat(message):
    if not ai_model:
        bot.reply_to(message, "مرحباً ديفيد! النظام يعمل ولكن مفتاح الذكاء الاصطناعي بحاجة للتأكيد.")
        return
    
    try:
        prompt = f"أنت مساعد خبير ومحترف في الجيوماتكس، المساحة، نظم المعلومات الجغرافية GIS، ولغة بايثون للخرائط (ArcPy). أجب باحترافية على السؤال التالي باللغة العربية: {message.text}"
        response = ai_model.generate_content(prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "عذراً، حدث خطأ مؤقت أثناء معالجة طلبك عبر الذكاء الاصطناعي.")

if __name__ == "__main__":
    print("Bot is running perfectly...")
    bot.infinity_polling()
