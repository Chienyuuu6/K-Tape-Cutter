from telegram.ext import (
    ContextTypes,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackQueryHandler,
)
from io import BytesIO
import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import qrcode

# Conversation entry point
LENGTH, INNER, SHOWING = range(3)
tape_format = ''
tape_length, tape_inner = 0 , 0



logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    context.user_data.clear()

    await context.bot.send_message(
        text=f'HI {update.message.from_user.first_name}👋🏻\n我是KTape Cutter Genie',
        chat_id=update.message.chat.id,
    )


    keyboard = [
        [InlineKeyboardButton("基本修邊", callback_data="tape1")],
        [InlineKeyboardButton("單邊開Y", callback_data="tape2")],
        [InlineKeyboardButton("雙邊開Y", callback_data="tape3")],
        [InlineKeyboardButton("網狀消腫", callback_data="tape4")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('請選擇要剪裁的肌貼樣式:', reply_markup=reply_markup)

    return LENGTH


async def length(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    format_type = query.data
    global tape_format
    tape_format = format_type
    print(tape_format)

    await update.callback_query.message.reply_text('輸入要剪裁的肌貼長度(格數)')   

    if(tape_format == "tape1"):
        global tape_inner
        tape_inner=0
        print(tape_inner)
        return SHOWING
    else:
        return INNER

async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = update.message
    global tape_length
    if(message.text=="/start"):
        return ConversationHandler.END
    try:
        tape_length = int(message.text)

    except ValueError:
        await update.message.reply_text('請輸入有效的整數，請重新輸入：')
        return INNER
    
    print(tape_length)
    print(tape_format)

    await update.message.reply_text('輸入要開Y/網狀的長度(格數)')
    return SHOWING
        
    
        



async def show_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    global tape_inner, tape_length
    if(tape_format!="tape1"):
        if(message.text=="/start"):
            return ConversationHandler.END
        try:
            tape_inner = int(message.text)
            

        except ValueError:
            await update.message.reply_text('請輸入有效的整數，請重新輸入：')
            return SHOWING
    else:
        try:
            tape_length = int(message.text)

        except ValueError:
            await update.message.reply_text('請輸入有效的整數，請重新輸入：')
            return SHOWING
        print(type(tape_length))
    



    #query = update.callback_query

    json_dict = {
        "format": tape_format,
        "length": tape_length,
        "inner": tape_inner
    }

    print(json_dict)
    

    json_data = json.dumps(json_dict, indent=2)
    data = json.loads(json_data)

    state_format = {
        "tape1": "基本修邊",
        "tape2": "單邊開Y",
        "tape3": "雙邊開Y",
        "tape4": "網狀消腫"
    }
    
    await update.message.reply_text(
        text=f"您所要求的肌貼形式/長度:\n\n肌貼形式: {state_format[tape_format]}\n肌貼長度: {tape_length}\n開Y/網狀長度: {tape_inner}"
    )

    # 產生QRcode並回傳telegram-bot
    img = qrcode.make(data)
    bio = BytesIO()
    bio.name = 'image.png'
    img.save(bio, 'PNG')
    bio.seek(0)
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=bio)
    await update.message.reply_text("請在K-Tape Cutter Machine 掃描此 QR code :)")
    return ConversationHandler.END


if __name__ == '__main__':
    application = ApplicationBuilder().token("6926390124:AAGPxrW6qkVeOuo2QrgzPiquzsJmCnEqU7s").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LENGTH: [CallbackQueryHandler(length)],
            INNER: [MessageHandler(filters.TEXT,inner)],
            SHOWING: [MessageHandler(filters.TEXT,show_data)]
        },
        fallbacks=[CommandHandler("start", start)]
    )

    application.add_handler(conv_handler)
    application.run_polling()
