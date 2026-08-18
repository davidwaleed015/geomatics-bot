import os
import sqlite3
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# التوكن الأساسي للبوت
TELEGRAM_BOT_TOKEN = "8605350892:AAEQARoXq3LJHuQULCqeHhRQqFj6DeutxKM"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

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
        f"✨ لديك **({trials})** تجارب مجانية للاستعلام الهندسي.\n"
        f"👇 **اختر القسم المناسب لعملك من القائمة أدناه:**"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=main_menu_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    bot.answer_callback_query(call.id)
    
    if call.data == "main_menu":
        bot.edit_message_text("🌐 **القائمة الرئيسية للمنصة:**\nاختر أحد الأقسام أدناه:", call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=main_menu_keyboard())

    elif call.data == "survey_devices":
        text = (
            "📡 **قسم الأجهزة المساحية والمعايرة:**\n\n"
            "• **Total Station:** شاشات التشغيل، القياسات الرصدية، وتصحيح أخطاء التوجيه.\n"
            "• **GPS / GNSS:** إعدادات الـ RTK، ربط الشبكات الجيوديسية، وتحويل الإحداثيات.\n"
            "• **Digital Level:** الموازنات الدقيقة وحساب مناسيب النقاط بدقة عالية."
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())

    elif call.data == "remote_sensing":
        text = (
            "🌍 **قسم الاستشعار عن بعد (Remote Sensing):**\n\n"
            "• **برنامج ENVI:** معالجة الصور الفضائية المتقدمة والتحليل الطيفي.\n"
            "• **برنامج ERDAS Imagine:** التصحيح الهندسي للمرئيات وتصنيف الصور (Image Classification).\n"
            "• **مؤشرات الغطاء النباتي:** حساب مؤشرات (NDVI, NDWI) بدقة."
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())

    elif call.data == "gis_software":
        text = (
            "💻 **برامج الـ GIS وتطبيقات البايثون:**\n\n"
            "• **ArcGIS Pro:** بناء قواعد البيانات الجغرافية (Geodatabases) والتحليل المكاني.\n"
            "• **QGIS:** الخرائط الرقمية المفتوحة وتكامل الإضافات البرمجية.\n"
            "• **Python & ArcPy:** أتمتة المهام واستخراج التقارير آلياً."
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())

    elif call.data == "civil_roads":
        text = (
            "🛣️ **قسم تصميم الطرق (AutoCAD Civil 3D):**\n\n"
            "• إنشاء مسارات الطرق المحورية (Alignments) والقطاعات الطولية (Profiles).\n"
            "• تصميم القطاعات العرضية (Assemblies & Corridors).\n"
            "• حساب كميات الحفر والردم (Earthwork Quantities)."
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())

    elif call.data == "software_hub":
        text = (
            "📦 **مستودع البرامج المتاحة (Software Hub):**\n\n"
            "إليك روابط تحميل أهم برامج المجال (مع التفعيل):\n"
            "1. **ArcGIS Pro:** [تحميل مباشر](https://example.com/arcgis)\n"
            "2. **AutoCAD Civil 3D:** [تحميل مباشر](https://example.com/civil3d)\n"
            "3. **ENVI & ERDAS:** [تحميل مباشر](https://example.com/envi-erdas)\n"
            "4. **QGIS:** [الموقع الرسمى](https://qgis.org)"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())

    elif call.data == "master_corner":
        text = (
            "🎓 **ركن الماجستير والأبحاث الأكاديمية:**\n\n"
            "• مقترحات أبحاث رسائل الماجستير والدكتوراه في الجيوماتكس ونظم المعلومات.\n"
            "• مراجع مساحية وكتب علمية متخصصة.\n"
            "• مصادر قواعد بيانات مكانية عالمية مجانية."
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())

    elif call.data == "dev_tools":
        text = (
            "🛠️ **أدوات المطورين وسكربتات الأتمتة:**\n\n"
            "إليك كود بايثون سريع للتحقق من الطبقات الجغرافية:\n"
            "```python\nimport arcpy\narcpy.env.workspace = 'C:/Data'\nfc_list = arcpy.ListFeatureClasses()\nprint(fc_list)\n```"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())

    elif call.data == "vip_plans":
        text = (
            "💎 **تفاصيل باقات الاشتراك الاحترافية (VIP 1 إلى VIP 5):**\n\n"
            "🔹 **VIP 1 - الباقة الأساسية:** تشمل الأجهزة المساحية وأساسيات الـ GIS.\n"
            "🔹 **VIP 2 - الباقة المتقدمة:** أساسيات الـ GIS + الاستشعار عن بعد (ENVI & ERDAS).\n"
            "🔹 **VIP 3 - الباقة الاحترافية:** الاستشعار عن بعد + تصميم الطرق ببرنامج Civil 3D.\n"
            "🔹 **VIP 4 - باقة ركن الماجستير:** المراجع الأكاديمية والدعم البحثي وتحليل البيانات.\n"
            "🔹 **VIP 5 - الباقة الشاملة (All-In-One):** الوصول الكامل لكل الأقسام البرمجية وأكواد الأتمتة."
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())

    elif call.data == "support":
        text = (
            "💳 **الدعم الفني وفودافون كاش:**\n\n"
            "لإتمام الاشتراك في أي باقة VIP، يرجى التحويل على المحفظة الرسمية:\n"
            "📲 **رقم المحفظة:** `01012345678`\n\n"
            "ثم أرسل صورة إيصال التحويل هنا لتفعيل حسابك فوراً."
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())

@bot.message_handler(func=lambda message: True)
def handle_text_chat(message):
    text = message.text
    response_msg = (
        f"🤖 **رد مساعد الجيوماتكس:**\n\n"
        f"لقد استلمت استفسارك حول: *({text})*.\n"
        f"بصفتي مساعدك الهندسي، أنصحك بمراجعة **أقسام الأجهزة المساحية** أو **برامج الـ GIS** من القائمة الرئيسية، أو تصفح الأكواد المتاحة في أدوات المطورين للحصول على النتيجة الدقيقة!"
    )
    bot.reply_to(message, response_msg, parse_mode="Markdown")

if __name__ == "__main__":
    print("Bot is running perfectly...")
    bot.infinity_polling()
