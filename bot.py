import os
import sqlite3
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# توكن البوت الأساسي
TELEGRAM_BOT_TOKEN = "8605350892:AAEQAroXq3LJHuQULCqeHhROQfj6DeutxkM"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# تهيئة قاعدة البيانات المحلية للمستخدمين
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

# أزرار القائمة الرئيسية المنسقة
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
    welcome_text = f"🌐 **مرحباً بك يا {username} في المنصة الهندسية المتكاملة (Geomatics Copilot)**\n\n✨ لديك **({trials})** تجارب مجانية.\n👇 اختر القسم المناسب لعملك من القائمة أدناه:"
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=main_menu_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    bot.answer_callback_query(call.id)
    if call.data == "main_menu":
        bot.edit_message_text("🌐 **القائمة الرئيسية للمنصة:**\nاختر أحد الأقسام أدناه:", call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=main_menu_keyboard())
    elif call.data == "survey_devices":
        bot.edit_message_text("📡 **قسم الأجهزة المساحية والمعايرة:**\n• Total Station: ضبط أخطاء التوجيه والرصد.\n• GNSS: إعدادات RTK وتحويل الإحداثيات.\n• Digital Level: الموازنات الدقيقة.", call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())
    elif call.data == "remote_sensing":
        bot.edit_message_text("🌍 **قسم الاستشعار عن بعد:**\n• ENVI & ERDAS Imagine للمعالجة الفضائية والتصنيف الطيفي.", call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())
    elif call.data == "gis_software":
        bot.edit_message_text("💻 **برامج الـ GIS وتطبيقات البايثون:**\n• ArcGIS Pro & QGIS وقواعد البيانات الجغرافية.", call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())
    elif call.data == "civil_roads":
        bot.edit_message_text("🛣️ **تصميم الطرق (Civil 3D):**\n• المسارات، القطاعات الطولية والعرضية، وحساب كميات الحفر والردم.", call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())
    elif call.data == "software_hub":
        bot.edit_message_text("📦 **مستودع البرامج والتحميلات:**\n• روابط تحميل برامج المجال والروابط المباشرة.", call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())
    elif call.data == "master_corner":
        bot.edit_message_text("🎓 **ركن الماجستير والأبحاث الأكاديمية:**\n• مقترحات أبحاث الماجستير والمراجع المساحية المتخصصة.", call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())
    elif call.data == "dev_tools":
        bot.edit_message_text("🛠️ **أدوات المطورين وسكربتات الأتمتة:**\n• سكربتات بايثون جاهزة لمهام الـ GIS.", call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())
    elif call.data == "vip_plans":
        bot.edit_message_text("💎 **باقات VIP الاحترافية (1 إلى 5):**\n• باقات مخصصة للتحكم الكامل والوصول الشامل.", call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())
    elif call.data == "support":
        bot.edit_message_text("💳 **الدعم الفني وفودافون كاش:**\n• رقم المحفظة: `01012345678`\nأرسل إيصال التحويل هنا لتفعيل حسابك.", call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())

@bot.message_handler(func=lambda message: True)
def handle_text_chat(message):
    text = message.text
    response_msg = f"🔍 أهلاً بك يا ديفيد! استفسارك حول ({text}) في مجال المساحة والجيوماتكس تم تسجيله، ويمكنك تصفح الأقسام عبر القائمة أو التواصل المباشر مع الدعم الفني."
    bot.reply_to(message, response_msg)

if __name__ == "__main__":
    print("Bot is running perfectly...")
    bot.infinity_polling()
