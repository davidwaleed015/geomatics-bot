# -*- coding: utf-8 -*-
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# --- الإعدادات الأساسية ---
TOKEN = "8605350892:AAEQAroXq3LJHuQULCqeHhROQfj6DeutxkM"
PAYMENT_NUMBER = "01277751915"

# --- القاموس المركزي لبيانات الباقات ---
PACKAGES = {
    "vip1": {"name": "VIP 1 - الأساسية", "prices": "شهري: 300 EGP | ربع سنوي: 800 EGP | نصف سنوي: 1,500 EGP | سنوي: 2,800 EGP"},
    "vip2": {"name": "VIP 2 - المتقدمة", "prices": "شهري: 500 EGP | ربع سنوي: 1,350 EGP | نصف سنوي: 2,500 EGP | سنوي: 4,800 EGP"},
    "vip3": {"name": "VIP 3 - الإحترافية", "prices": "شهري: 800 EGP | ربع سنوي: 2,150 EGP | نصف سنوي: 4,000 EGP | سنوي: 7,500 EGP"},
    "master": {"name": "🎓 ركن الماجستير", "prices": "شهري: 1,500 EGP | ربع سنوي: 4,050 EGP | نصف سنوي: 7,600 EGP | سنوي: 14,000 EGP"},
    "dev": {"name": "💻 أدوات المطورين", "prices": "شهري: 1,000 EGP | ربع سنوي: 2,700 EGP | نصف سنوي: 5,000 EGP | سنوي: 9,500 EGP"}
}

# --- إدارة قاعدة البيانات لتتبع الاستخدام والتجارب المجانية ---
def init_db():
    conn = sqlite3.connect('geomatics_bot.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, free_trials INTEGER DEFAULT 2)''')
    conn.commit()
    conn.close()

# --- القوائم الرئيسية والفرعية (منظمة لتسهيل التعديل) ---
def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📐 الأجهزة المساحية", callback_data="menu_survey"),
         InlineKeyboardButton("🌍 الاستشعار عن بعد", callback_data="menu_rs")],
        [InlineKeyboardButton("💻 برامج الـ GIS والخرائط", callback_data="menu_gis"),
         InlineKeyboardButton("🛣️ مساعد تصميم الطرق", callback_data="menu_roads")],
        [InlineKeyboardButton("🎓 ركن الماجستير", callback_data="menu_master"),
         InlineKeyboardButton("⚙️ أدوات المطورين (مدفوع)", callback_data="menu_dev")],
        [InlineKeyboardButton("🎬 صانع الفيديوهات", callback_data="menu_video"),
         InlineKeyboardButton("💎 باقات الاشتراك VIP", callback_data="menu_vip")],
        [InlineKeyboardButton("📞 الدعم وفودافون كاش", callback_data="menu_contact")]
    ])

# --- نقطة البداية ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conn = sqlite3.connect('geomatics_bot.db')
    c = conn.cursor()
    c.execute("SELECT free_trials FROM users WHERE id = ?", (user_id,))
    row = c.fetchone()
    if not row:
        c.execute("INSERT INTO users (id, free_trials) VALUES (?, 2)", (user_id,))
        conn.commit()
    conn.close()

    text = (
        "🌐 *مرحباً بك في Geomatics Copilot - النسخة الاحترافية المنظمة*\n\n"
        "✨ لديك (2) تجارب مجانية لتحليل الخرائط قبل طلب الاشتراك.\n"
        "اختر أحد الأقسام أدناه للبدء:"
    )
    await update.message.reply_text(text, reply_markup=get_main_menu(), parse_mode="Markdown")

# --- معالج الأزرار والتنقل السلس ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    if data == "menu_survey":
        kb = [
            [InlineKeyboardButton("Leica Total Station", callback_data="sub_total"),
             InlineKeyboardButton("Sokkia / Topcon", callback_data="sub_sokkia")],
            [InlineKeyboardButton("أجهزة GPS / GNSS RTK", callback_data="sub_gps"),
             InlineKeyboardButton("ميزان القامة (Level)", callback_data="sub_level")],
            [InlineKeyboardButton("ماسح الليزر (LiDAR)", callback_data="sub_lidar"),
             InlineKeyboardButton("الدرونز المساحية (UAVs)", callback_data="sub_drone")],
            [InlineKeyboardButton("التيودوليت (Theodolite)", callback_data="sub_theodolite")],
            [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="back_main")]
        ]
        await query.edit_message_text("🔭 *قسم الأجهزة المساحية والقوائم الفرعية:*", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif data == "menu_rs":
        kb = [
            [InlineKeyboardButton("تحميل المعالجة الفضائية (Landsat/Sentinel)", callback_data="rs_download")],
            [InlineKeyboardButton("تصنيف المرئيات (Image Classification)", callback_data="rs_class")],
            [InlineKeyboardButton("حساب المؤشرات (NDVI/NDWI)", callback_data="rs_indices")],
            [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="back_main")]
        ]
        await query.edit_message_text("🌍 *قسم الاستشعار عن بعد (Remote Sensing):*", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif data == "menu_gis":
        kb = [
            [InlineKeyboardButton("ArcGIS Pro", callback_data="gis_arc"),
             InlineKeyboardButton("QGIS & Python Automation", callback_data="gis_qgis")],
            [InlineKeyboardButton("AutoCAD Civil 3D", callback_data="gis_civil"),
             InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="back_main")]
        ]
        await query.edit_message_text("💻 *برامج الـ GIS والخرائط الهندسية:*", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif data == "menu_dev":
        kb = [
            [InlineKeyboardButton("أدوات الأتمتة البرمجية وتطوير السكربتات (API)", callback_data="dev_tools")],
            [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="back_main")]
        ]
        await query.edit_message_text("⚙️ *قائمة المطورين (مدفوعة):*\nأدوات برمجية متقدمة لتطوير تطبيقات الجيوماتكس.", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif data == "menu_vip":
        text = "💎 *باقات الاشتراك VIP المتاحة (شهري / ربع سنوي / نصف سنوي / سنوي):*\n\n"
        for k, p in PACKAGES.items():
            text += f"🔹 *{p['name']}*\n   {p['prices']}\n\n"
        kb = [[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="back_main")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif data == "menu_contact":
        text = (
            f"📞 *الدعم الفني وفودافون كاش*\n\n"
            f"• رقم التحويل المعتمد: `{PAYMENT_NUMBER}`\n"
            f"• أرسل صورة إيصال التحويل هنا بعد التحويل ليتم تفعيل حسابك واشتراكك فوراً."
        )
        kb = [[InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="back_main")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif data == "back_main":
        await query.edit_message_text("🌐 *القائمة الرئيسية - Geomatics Copilot*", reply_markup=get_main_menu(), parse_mode="Markdown")

# --- تشغيل التطبيق ---
if __name__ == '__main__':
    init_db()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Geomatics Copilot Clean & Optimized Version Running!")
    app.run_polling()