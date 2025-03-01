import logging
from telegram import (
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, Update, InputFile
)
from telegram.ext import (
    Application, CommandHandler, ContextTypes,
    ConversationHandler, MessageHandler, filters
)

# 🛠 Logging sozlamalari
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# 🔑 TOKEN va ADMIN ID
TOKEN = "7570796885:AAGkiK-QBSSfmrOslR0KsddUE_LeeCUuBNY"
ADMIN_ID = 6578706277  # ID butun son (int) bo‘lishi kerak

# 📌 Holatlar uchun o‘zgaruvchilar
NAME, DISTRICT, PHONE, CHILD_AGE, FEEDBACK = range(5)

# 📌 Klaviatura tugmalari
main_menu = ReplyKeyboardMarkup(
    [
        ["Ro'yxatdan o'tish", "Loyiha haqida"],
        ["Kitoblar bo‘limi", "Fikr va maslahatlar"],
    ],
    one_time_keyboard=True,
    resize_keyboard=True,
)

# 📌 /start buyrug‘i
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "👋 Assalomu alaykum! 'KITOBXON KIDS' botiga xush kelibsiz!", reply_markup=main_menu
    )
    return ConversationHandler.END

# 📋 Ro‘yxatdan o‘tish
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("📌 Ism va familiyangizni kiriting:")
    return NAME

async def name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["name"] = update.message.text
    districts = [["Shayxontohur", "Chilonzor", "Yunusobod"],
                 ["Olmazor", "Bektemir", "Yakkasaroy"],
                 ["Uchtepa", "Sergeli", "Mirzo Ulug‘bek"],
                 ["Zangiota", "Yangiyo‘l", "Chirchiq"]]
    markup = ReplyKeyboardMarkup(districts, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("🏙 Tumanni tanlang:", reply_markup=markup)
    return DISTRICT

async def district(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["district"] = update.message.text
    keyboard = [[KeyboardButton("📞 Raqamni ulashish", request_contact=True)]]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("📞 Telefon raqamingizni ulashing:", reply_markup=markup)
    return PHONE

async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["phone"] = update.message.contact.phone_number
    age_buttons = [["7", "8", "9", "10"]]
    markup = ReplyKeyboardMarkup(age_buttons, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("📅 Bolaning yoshini tanlang:", reply_markup=markup)
    return CHILD_AGE

async def child_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["child_age"] = update.message.text
    await update.message.reply_text("✅ Ro‘yxatdan o‘tish muvaffaqiyatli yakunlandi!", reply_markup=main_menu)

    # 📨 Admin ga xabar yuborish
    message = (
        f"📩 Yangi ro'yxatdan o'tish:\n"
        f"👤 Ism: {context.user_data['name']}\n"
        f"🏙 Tuman: {context.user_data['district']}\n"
        f"📞 Telefon: {context.user_data['phone']}\n"
        f"📅 Yosh: {context.user_data['child_age']}"
    )
    await context.bot.send_message(chat_id=ADMIN_ID, text=message)
    return ConversationHandler.END

# 📚 Loyiha haqida
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("📖 'KITOBXON KIDS' loyihasi haqida ma'lumot...")

# 📚 Kitoblar bo‘limi
async def books(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [["📚 Kitob 1", "📚 Kitob 2"], ["📚 Kitob 3", "📚 Kitob 4"]]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("📚 Kitoblarni tanlang:", reply_markup=markup)

async def book_detail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    book_name = update.message.text
    if book_name == "📚 Kitob 1":
        pdf_path = "kitoblar/kitob1.pdf"
        audio_path = "kitoblar/kitob1.mp3"
        image_path = "kitoblar/kitob1.jpg"

        with open(pdf_path, "rb") as pdf, open(audio_path, "rb") as audio, open(image_path, "rb") as img:
            await update.message.reply_photo(photo=InputFile(img), caption="📖 Kitob 1")
            await update.message.reply_document(document=InputFile(pdf), caption="📄 PDF fayl")
            await update.message.reply_audio(audio=InputFile(audio), caption="🎧 Audio versiya")

# 💬 Fikr va maslahatlar boshlash
async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("💬 Fikr va maslahatlaringizni kiriting:")
    return FEEDBACK

# 💬 Fikrni qabul qilish va adminga yuborish
async def get_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    feedback_text = update.message.text
    user = update.message.from_user

    # Foydalanuvchiga tasdiqlash xabarini yuborish
    await update.message.reply_text("✅ Fikringiz uchun rahmat!", reply_markup=main_menu)

    # 📨 Admin ga fikr yuborish
    feedback_message = (
        f"📩 Yangi fikr:\n"
        f"👤 Foydalanuvchi: {user.full_name} (@{user.username})\n"
        f"💬 Fikr: {feedback_text}"
    )
    await context.bot.send_message(chat_id=ADMIN_ID, text=feedback_message)
    return ConversationHandler.END

# 🔄 Botni ishga tushirish
def main() -> None:
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^Ro'yxatdan o'tish$"), register)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
            DISTRICT: [MessageHandler(filters.TEXT & ~filters.COMMAND, district)],
            PHONE: [MessageHandler(filters.CONTACT, phone)],
            CHILD_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, child_age)],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    feedback_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^Fikr va maslahatlar$"), feedback)],
        states={FEEDBACK: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_feedback)]},
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex("^Loyiha haqida$"), about))
    application.add_handler(MessageHandler(filters.Regex("^Kitoblar bo‘limi$"), books))
    application.add_handler(MessageHandler(filters.Regex("^📚 Kitob [1-4]$"), book_detail))
    
    application.add_handler(conv_handler)
    application.add_handler(feedback_handler)

    application.run_polling()

if __name__ == "__main__":
    main()
    
# ❌ Notanish buyruqlar
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("❌ Noto‘g‘ri buyruq. Iltimos, menyudan foydalaning.")

# 🔄 Botni ishga tushirish
def main() -> None:
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^Ro'yxatdan o'tish$"), register)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
            DISTRICT: [MessageHandler(filters.TEXT & ~filters.COMMAND, district)],
            PHONE: [MessageHandler(filters.CONTACT, phone)],
            CHILD_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, child_age)],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex("^Loyiha haqida$"), about))
    application.add_handler(MessageHandler(filters.Regex("^Kitoblar bo‘limi$"), books))
    application.add_handler(MessageHandler(filters.Regex("^📚 Kitob [1-4]$"), book_detail))
    
    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()
