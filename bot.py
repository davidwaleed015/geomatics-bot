import os
import sqlite3
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# التوكن الصحيح المعمد لبوت Geomatics Helper Bot
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
    keyboard.row(InlineKeyboardButton("📡 الأجهزة المساحية (توتال، ليزر سكانر، درونز، GPS)", callback_data="all_survey_devices"))
    keyboard.row(InlineKeyboardButton("💻 البرامج المساحية (Civil 3D, Surfer, Carlson, Excel)", callback_data="all_survey_software"))
    keyboard.row(InlineKeyboardButton("🌍 GIS والاستشعار (ArcGIS Pro, QGIS, ENVI, ERDAS)", callback_data="gis_remote_pro"))
    keyboard.row(InlineKeyboardButton("🛣️ تصميم الطرق والمشاريع الهندسية", callback_data="civil_roads"))
    keyboard.row(InlineKeyboardButton("📦 مستودع التحميلات والسوفتوير (Software Hub)", callback_data="software_hub"))
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
        f"👇 **اختر القسم المطلوب من القائمة الشاملة أدناه:**"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=main_menu_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    bot.answer_callback_query(call.id)
    
    if call.data == "main_menu":
        bot.edit_message_text("🌐 **القائمة الرئيسية الشاملة:**\nاختر أحد الأقسام أدناه:", call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=main_menu_keyboard())

    elif call.data == "all_survey_devices":
        text = (
            "📡 **قسم الأجهزة المساحية المتقدمة:**\n\n"
            "• **Total Station (التوتال ستيشن):** شاشات التشغيل، الرصد والتوجيه، حساب الإحداثيات، وتصحيح الأخطاء.\n"
            "• **GNSS / GPS (مستقبلات الأقمار):** إعدادات الـ RTK، ربط الشبكات الجيوديسية الثابتة والمتحركة.\n"
            "• **3D Laser Scanner (الماسح الضوئي):** التوثيق المعماري، السحب النقدي (Point Clouds)، والنمذجة.\n"
            "• **Drones (الدرونز / المسح الجوي):** تصوير الرفع المساحي بالدرون، إنتاج الخرائط الكنتورية والـ Orthomosaic.\n"
            "• **Digital & Auto Level (الموازنات):** الموازنات الدقيقة لحساب فروق المناسيب وشبكات الترتيب الهندسي."
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())

    elif call.data == "all_survey_software":
        text = (
            "💻 **البرامج المساحية والهندسية المتخصصة:**\n\n"
            "• **AutoCAD & Civil 3D:** رسم اللوحات، التصميم الأفقي والرأسي، والقطاعات.\n"
            "• **Surfer:** معالجة النماذج الرقمية لارتفاعات الـ DEM وخرائط الكونتور وتحساب الحفريات.\n"
            "• **ProLink & Leica Geo Office:** تفريغ ومعالجة بيانات الأجهزة المساحية (Leica, Trimble, Sokkia).\n"
            "• **Carlson Survey:** أقوى إضافات المساحة والرفع والتوقيع لبرامج الأوتوكاد.\n"
            "• **SketchUp:** النمذجة ثلاثية الأبعاد للمشاريع المعمارية والمساحية.\n"
            "• **Microsoft Excel (للمساحين):** جداول حساب الكميات، تحويل الإحداثيات، وتصميم جداول التوقيع."
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())

    elif call.data == "gis_remote_pro":
        text = (
            "🌍 **قسم نظم المعلومات الجغرافية (GIS) والاستشعار عن بعد (الشامل):**\n\n"
            "🔷 **أولاً: برامج نظم المعلومات الجغرافية (GIS):**\n"
            "• **ArcGIS Desktop (ArcMap):** البرنامج الكلاسيكي لإدارة قواعد البيانات الجغرافية والتحليل المكاني (مدفوع).\n"
            "• **ArcGIS Pro:** المنصة الحديثة المتكاملة للربط الثنائي والثلاثي الأبعاد والـ Web GIS (مدفوع).\n"
            "• **QGIS:** أقوى البرامج المفتوحة ومجانية المصدر للخرائط والتحليل المكاني (مجاني).\n"
            "• **Global Mapper:** معالجة البيانات المساحية الضخمة، تحويل الصيغ، وفتح الـ DEM (مدفوع).\n\n"
            "🛰️ **ثانياً: برامج الاستشعار عن بعد والمعالجة:**\n"
            "• **ENVI:** المعالجة الطيفية المتقدمة للصور الفضائية وتحليل النطاقات (مدفوع).\n"
            "• **ERDAS Imagine:** التصحيح الهندسي، التصنيف المراقب وغير المراقب للمرئيات (مدفوع).\n"
            "• **PCI Geomatica (Catalyst):** معالجة صور الأقمار والصور الرادارية SAR (مدفوع).\n"
            "• **SNAP:** برنامج وكالة الفضاء الأوروبية لمعالجة صور سنتينل (مجاني)."
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())

    elif call.data == "civil_roads":
        text = (
            "🛣️ **تصميم الطرق والمشاريع (Civil 3D & Roads):**\n\n"
            "• إنشاء مسارات الطرق المحورية (Alignments).\n"
            "• إعداد القطاعات الطولية (Profiles) والعرضية (Assemblies & Corridors).\n"
            "• استخراج جداول كميات الحفر والردم (Cut & Fill Earthwork Tables)."
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())

    elif call.data == "software_hub":
        text = (
            "📦 **مستودع التحميلات والسوفتوير (Software Hub):**\n\n"
            "روابط تحميل برامج المجال والروابط المباشرة (مع الكراك والتفعيل):\n"
            "1. **ArcGIS Pro & ArcMap:** [روابط التنزيل والتفعيل](https://example.com/arcgis)\n"
            "2. **ENVI & ERDAS Imagine:** [روابط برامج الاستشعار](https://example.com/envi-erdas)\n"
            "3. **Civil 3D & AutoCAD:** [روابط التنزيل والتفعيل](https://example.com/autocad)\n"
            "4. **Global Mapper, Surfer & QGIS:** [برامج التحليل](https://example.com/tools)"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())

    elif call.data == "master_corner":
        text = (
            "🎓 **ركن الماجستير والأبحاث الأكاديمية:**\n\n"
            "• مقترحات أبحاث رسائل الماجستير والدكتوراه في الجيوماتكس ونظم المعلومات.\n"
            "• مراجع مساحية وكتب علمية متخصصة في الجيوديسيا.\n"
            "• مصادر قواعد بيانات مكانية عالمية مجانية للباحثين."
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())

    elif call.data == "dev_tools":
        text = (
            "🛠️ **أدوات المطورين وسكربتات الأتمتة:**\n\n"
            "إليك كود بايثون سريع لمعالجة ملفات الإحداثيات (CSV to Shapefile):\n"
            "```python\nimport arcpy\n# كود أتمتة لرفع الإحداثيات\nprint('GIS Automation Ready')\n```"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())

    elif call.data == "vip_plans":
        text = (
            "💎 **تفاصيل باقات الاشتراك الاحترافية (VIP 1 إلى VIP 5):**\n\n"
            "🔹 **VIP 1 (الباقة الأساسية):** تشمل الأجهزة المساحية (توتال وجي بي إس) وجداول الإكسيل.\n"
            "🔹 **VIP 2 (باقة البرامج المساحية):** تشمل (Surfer, AutoCAD, ProLink, Carlson).\n"
            "🔹 **VIP 3 (باقة نظم المعلومات والاستشعار):** (ArcGIS Pro, ArcMap, QGIS, ENVI, ERDAS).\n"
            "🔹 **VIP 4 (باقة الطرق والماجستير):** (Civil 3D والأبحاث الأكاديمية ورسائل الماجستير).\n"
            "🔹 **VIP 5 (الباقة الشاملة All-In-One):** الوصول الكامل لكل الأقسام، الدرونز، الليزر سكانر، وكامل السوفتوير والكراكات."
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())

    elif call.data == "support":
        text = (
            "💳 **الدعم الفني وفودافون كاش:**\n\n"
            "لإتمام الاشتراك في باقات VIP الهندسية، يرجى التحويل على محفظة فودافون كاش الرسمية:\n"
            "📲 **رقم المحفظة:** `01012345678`\n\n"
            "ثم أرسل صورة إيصال التحويل هنا لتفعيل حسابك وصلاحياتك فوراً."
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=back_to_main_keyboard())

@bot.message_handler(func=lambda message: True)
def handle_text_chat(message):
    text = message.text
    response_msg = (
        f"🤖 **رد مساعد الجيوماتكس الشامل:**\n\n"
        f"تم استلام استفسارك حول: *({text})*.\n"
        f"اختر القسم المطلوب من القائمة الرئيسية (سواء الباقات، الـ GIS، أو الدعم الفني) لتجد كل التفاصيل الفنية فوراً!"
    )
    bot.reply_to(message, response_msg, parse_mode="Markdown")

if __name__ == "__main__":
    print("Bot is running perfectly...")
    bot.infinity_polling()
