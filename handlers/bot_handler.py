from datetime import datetime
from math import prod
from telebot import TeleBot
from database.database import Database
# from users.utils.utils import *
from keyboard.keyboards import *
from telebot import types
import re
import jdatetime
import uuid
import os
import time
from telegram.constants import ParseMode

# bot = TeleBot("6352431084:AAGI80rFHKtlswbn1UOWnXJSrHVv4sVHU8Y")
bot = TeleBot("6698930799:AAEjdUGra1TwdTHDaeqrugrTUfnWnGy9n1M")
db = Database("bot.db")


def generate_purchase_id():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = uuid.uuid4().int & (1<<32)-1
    return f"{timestamp}-{str(unique_id)}"

def check_user_in_the_channel(user_id):
    user_id = int(user_id) #replace this with user id number, if you already know it
    member = bot.get_chat_member(-1001855912026, user_id)
    if member.status == 'left': #If check variable isn't null, user is in the group
        return False
    else:
        return True



def admin_payment_verify(photo, caption, user):
    user=f'{user}'
    # inline keyboard to verify payment
    inline_keyboard_payment_verify = types.InlineKeyboardMarkup(row_width=1)
    agree_button = types.InlineKeyboardButton("تایید", callback_data=" دتایید "+user)
    disagree_button = types.InlineKeyboardButton("نامعتبر", callback_data=" نامعتبر "+user)
    inline_keyboard_payment_verify.add(agree_button, disagree_button)

    # Send the photo to the confirmation channel with the caption
    with open(photo, 'rb') as photo_to_send:
        bot.send_photo("1199074676", photo_to_send, caption=caption, reply_markup=inline_keyboard_payment_verify)

@bot.callback_query_handler(func=lambda query: 'دتایید' in query.data)
def payment_verified(query):
    print("hello")
    data : str = query.data
    result = [int(x) for x in data.split() if x.isdigit()]
    last_purchase = db.get_user_purchase(result[0])
    product_id= db.get_last_purchase_product_id(result[0])
    date = jdatetime.date.fromgregorian(day=datetime.today().day, month=datetime.today().month, year=datetime.today().year).strftime('%Y-%m-%d')
    expire = jdatetime.date.fromgregorian(day=datetime.today().day, month=datetime.today().month + last_purchase[0][5], year=datetime.today().year).strftime('%Y-%m-%d')
    db.update_purchase_status(last_purchase[0][0])
    db.update_purchase_date(date, expire, last_purchase[0][0])
    db.update_product_status(product_id)
    message_buy = f"خرید شما با موفقیت انجام شد✅ \n\n برای دریافت اطلاعات سرویس خود بر روی دکمه سرویس های من ضربه بزنید 💡 \n\n و برای یادگیری روند اتصال بر روی دکمه راهنما اتصال ضربه بزنید 💡 "
                
    db.update_purchase_status(last_purchase[0][0])
    db.update_product_status(product_id)
    bot.send_message(query.message.chat.id, "رسید تایید شد")
    bot.send_message(result[0], message_buy)

@bot.callback_query_handler(func=lambda query: 'نامعتبر' in query.data)
def payment_rejected(query):
    data : str = query.data
    result = [int(x) for x in data.split() if x.isdigit()]
    message_buy = ".متاسفانه رسید شما رد شد. در صورت اعتراض با پشتیبانی ارتباط برقرار کنید"
    bot.send_message(query.message.chat.id, message_buy)
    bot.send_message(result[0], message_buy)


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    first_name = message.from_user.first_name
    user_name = message.from_user.username
    wallet = 0
    joined = jdatetime.date.fromgregorian(day=datetime.today().day, month=datetime.today().month, year=datetime.today().year).strftime('%Y-%m-%d')
    response = f'سلام {first_name} \n چه کاری میتونم برات انجام بدم؟'
    bot.send_message(user_id, response, reply_markup=keyboard)
    db.insert_user(user_id, first_name, user_name, wallet, joined)


# @bot.message_handler(func=lambda message: message.text == 'لینک اتصال 🔗')
# def get_link(message):
#     user_id = message.chat.id
#     check = check_user_in_the_channel(user_id)
#     if check == False:
#         return bot.send_message(user_id, "برای استفاده از رباط عضو کانالمون شو و بعد امتحان کن \n t.me/")
#     confirmed_purchase = db.get_confirmed_purchase_by_user(user_id)
#     if len(confirmed_purchase) == 0:
#         return bot.send_message(user_id, "شما سرویس فعالی ندارید")
#     product = db.get_product_by_id(confirmed_purchase[2])
#     print(confirmed_purchase)
#     sub_link = product[3]
#     message_link = f"💡با لینک زیر میتونین به سرویس هاتون دسترسی پیدا کنید:\n{sub_link}\n\nاز طریق « راهنما اتصال » " \
#                    f"در منو بات ، روش متصل شدن به سرویس ما رو میتونید یاد بگیرید.\n\nبرای اطلاع از نوع سرویس و باقی " \
#                    f"مانده حساب خود ، روی « 🪪 اطلاعات سرویس » در منو بات کلیک کنید."
#     bot.send_message(user_id, message_link)


@bot.message_handler(func=lambda message: message.text == "🪪 سرویس های من")
def get_servise_info(message):
    user_id = message.chat.id
    check = check_user_in_the_channel(user_id)
    if check == False:
        return bot.send_message(user_id, "برای استفاده از رباط عضو کانالمون شو و بعد امتحان کن \n t.me/")
    user = db.get_user_by_id(user_id)[0]
    purchases = db.get_confirmed_purchase_by_user(user_id)
    if len(purchases) == 0:
        return bot.send_message(user_id, "شما سرویس فعالی ندارید")
    x = 1
    for purchase in purchases:
        product = db.get_product_by_id(purchase[2])[0]
        volume = purchase[7]
        user = purchase[8]
        plan_name = 'ساب'
        if product[1] == 'vless':
            plan_name = 'تک لینک'
        if product[1] == 'ssh':
            plan_name = 'S S H'
        if volume == 'limitless':
            volume = 'نامحدود'
        response = f'👨‍💻{x}-اطلاعات سرویس شما به شرح زیر میباشد.\n \n 💳 حجم سرویس(گیگ) : {volume} \n\n 💳 نوع کانفیگ : {plan_name} \n\n 💳 تعداد کاربر : {user} \n\n 🩵 آیدی خرید : \n \n {purchase[0]} \n 🩵 لینک اتصال : \n \n {product[3]} \n \n ⌛️تاریخ شروع سرویس: {purchase[4]}\n\n ⌛️تاریخ پایان سرویس: {purchase[9]}\n\n\n🕊'
        if product[1] == 'ssh':
            response = f'👨‍💻{x}-اطلاعات سرویس شما به شرح زیر میباشد.\n \n 💳 حجم سرویس(گیگ) : {volume} \n\n 💳 نوع کانفیگ : {plan_name} \n\n 💳 تعداد کاربر : {user} \n\n 🩵 آیدی خرید : \n \n {purchase[0]} \n 🩵 لینک اتصال : \n \n برای دریافت لینک اتصال خود این پیام را برای پشتیبانی فوروارد کنید \n\n 👷🏼‍♂️پشتیبانی: \n\n ⌛️تاریخ شروع سرویس: {purchase[4]}\n\n ⌛️تاریخ پایان سرویس: {purchase[9]}\n\n\n 🧩کانفیگ: {product[3]}'
        bot.send_message(user_id, response, reply_markup=keyboard_user_extend(purchase[0]))
        x+=1

@bot.callback_query_handler(func=lambda query: "تمدید" in query.data)
def extend_purchase(query):
    data = query.data
    choice = re.findall(r"'([^']*)'", data)
    old_purchase_id = choice[0]
    purchase = db.get_purchase_by_id(old_purchase_id)[0]
    duration = purchase[5]
    volume = purchase[7]
    user = purchase[8]
    purchase_id = generate_purchase_id()
    user_id = query.message.chat.id
    product = db.get_product_by_id(purchase[2])
    name = product[0][1]
    plan_name = 'ساب'
    if name == 'vless':
        plan_name = 'تک لینک'
    if name == 'ssh':
            plan_name = 'S S H'

    if volume == 'limitless':
        volume = 'نامحدود'
    if len(product)==0:
        return bot.send_message(user_id, ".محصول مورد نظر موجود نیست لطفا محصول دیگری انتخاب کنید یا تا موجود شدن آن صبر کنید .")
    status = "pending"
    price = purchase[6]
    date = jdatetime.date.fromgregorian(day=datetime.today().day, month=datetime.today().month, year=datetime.today().year).strftime('%Y-%m-%d')
    invoice_message = f"🧾تمدید سرویس با مشخصات:\n\n 💶قیمت: {price} ریال\n\n 💶حجم: {volume}\n\n 💶نوع کانفیگ: {plan_name}\n\n 💶مدت زمان: {duration} ماه\n\n 💶تعداد کاربر: {user} کاربره\n\n✅آیا مشخصات بالا مورد تأیید شماست؟"
    
    # insert to database
    db.insert_purchase(purchase_id, user_id, product[0][0], status, date, duration, price, volume, user, date)
    db.update_purchase_status_to_expired(old_purchase_id)
    bot.send_message(user_id, invoice_message, reply_markup=inline_keyboard_invoice)



@bot.message_handler(func=lambda message: message.text == "🪪پروفایل")
def get_user_info(message):
    user_id = message.chat.id
    check = check_user_in_the_channel(user_id)
    if check == False:
        return bot.send_message(user_id, "برای استفاده از رباط عضو کانالمون شو و بعد امتحان کن \n t.me/")
    user = db.get_user_by_id(user_id)[0]
    response = f'👨‍💻اطلاعات حساب کاربری شما به شرح زیر میباشد.\n \n 💳 موجودی شما : {user[3]} تومان \n 🩵 ایدی عددی شما : \n \n {user[0]} \n \n ⌛️تاریخ عضویت شما: {user[4]}'
    bot.send_message(user_id, response, reply_markup=inline_keyboard_user_charge)

@bot.callback_query_handler(func=lambda query: query.data == 'شارژ حساب')
def wallet_charge(query):
    user_id = query.message.chat.id
    check = check_user_in_the_channel(user_id)
    if check == False:
        return bot.send_message(user_id, "برای استفاده از رباط عضو کانالمون شو و بعد امتحان کن \n t.me/")
    
    message_buy = "برای شارژ حساب خود به اکانت پشتیبانی ما پیام بدید \n \n @hello"
    bot.send_message(user_id, message_buy)


@bot.message_handler(func=lambda message: message.text == "شارژ حساب 🔗")
def account_charge(message):
    user_id = message.chat.id
    check = check_user_in_the_channel(user_id)
    if check == False:
        return bot.send_message(user_id, "برای استفاده از رباط عضو کانالمون شو و بعد امتحان کن \n t.me/")
    message_buy = "برای شارژ حساب خود به اکانت پشتیبانی ما پیام بدید \n \n @hello"
    bot.send_message(user_id, message_buy)



message_sup = "👩‍💻 اکانت پاسخگویی و پشتیبانی⚡️:\n\n@hello\n\nSpeed is our signature"


@bot.message_handler(func=lambda message: message.text == "💬پشتیبانی")
def support(message):
    user_id = message.chat.id
    check = check_user_in_the_channel(user_id)
    if check == False:
        return bot.send_message(user_id, "برای استفاده از رباط عضو کانالمون شو و بعد امتحان کن \n t.me/")
    bot.send_message(message.chat.id, message_sup)

@bot.message_handler(func=lambda message: message.text == "سوالات متداول❓")
def questions(message):
    user_id = message.chat.id
    check = check_user_in_the_channel(user_id)
    if check == False:
        return bot.send_message(user_id, "برای استفاده از رباط عضو کانالمون شو و بعد امتحان کن \n t.me/")
    bot.send_message(chat_id = user_id, text = "\n\n<a href='t.me//21'>1-تعرفه اشتراک ها</a>\n\n<a href='t.me//294'>2-پشتیبانی</a>\n\nاتصال:\n\n<a href='t.me/hello/49'>3-اتصال به لینک اشتراک برای اندروید</a>\n\n<a href='t.me/hello/88'>4-برنامه مخصوص اندروید</a>\n\n<a href='t.me/hello/78'>5-آموزش آپدیت و اتصال به بهترین کانفیگ اندروید</a>\n\n<a href='t.me/hello/43'>6-اتصال برای آیفون(IOS+16)</a>\n\n<a href='t.me/hello/87'>7-آموزش آپدیت در FoXray</a>\n\n<a href='t.me/hello/85'>8-اتصال برای آیفون(IOS-16)</a>\n\n<a href='t.me/hello/87'>9-اتصال به بهترین کانفیگ در Fair Vpn</a>\n\n<a href='t.me/hello/79'>10-اتصال برای PC(IOS-16)</a>\n\n@hello", parse_mode = ParseMode.HTML)
# def questions(message):
    # message_FAQZ = "💩 Qi frequently asked questionzzz\n\n🔤 آیا سرویس‌های Qi آیپی ثابت هستند؟\n🔤 بله! با سرویس‌های " \
    #                "Qi به هیچ عنوان آیپی شما تغییر نخواهد کرد و تمامی سرور ها آیپی ثابت هستند. در صورت بروز بحران " \
    #                "ممکن است هر ۶ ماه یکبار آیپی عوض شود که در این صورت کشور ثابت می‌ماند.\n\n🔤 اگر سرور های Qi برای " \
    #                "مدتی در وضعیت update قرار بگیرند چه اتفاقی می افتد؟\n🔤 مقدار مصرف شده از سرویس کاربران در زمان " \
    #                "بروزرسانی بعد از اتمام آن به زمان تمدید کاربران اضافه خواهد شد.\n\n🔤 حجم و ترافیک هر سرویس " \
    #                "چقدره؟\n🔤 شما می توانید به میزان مصرف مورد نیاز خود ترافیک خریداری کنید.\n\n🔤 اگه به یک سرویس " \
    #                "بیشتر از حد مجاز متصل شویم چه اتفاقی می افتد؟\n🔤 در صورت اتصال بیشتر از میزان مجاز کانکشن " \
    #                "خریداری شده چه از نظر تعداد کاربر و چه از نظر حجم، سرویس شما مسدود خواهد شد.\n\n🔤 سرویس‌های Qi " \
    #                "سرعت اینترنت را بالا می برد؟\n🔤 سرویس ما همه اپراتور ها را برای افزایش سرعت پشتیبانی نمی کند ولی " \
    #                "بصورت کلی برای بعضی از اپراتور ها باعث افزایش سرعت می شود.\n\nSpeed is our signature\nConnect to " \
    #                "Qi (https://t.me/QIVPN) ⚡️"

    # bot.send_message(message.chat.id, message_FAQZ)


@bot.message_handler(func=lambda message: message.text == "📚راهنما اتصال")
def tutorials(message):
    user_id = message.chat.id
    check = check_user_in_the_channel(user_id)
    if check == False:
        return bot.send_message(user_id, "برای استفاده از رباط عضو کانالمون شو و بعد امتحان کن \n t.me/")
    bot.send_message(chat_id = user_id, text = "\n\n<a href='t.me//21'>1-تعرفه اشتراک ها</a>\n\n<a href='t.me//294'>2-پشتیبانی</a>\n\nاتصال:\n\n<a href='t.me/hello/49'>3-اتصال به لینک اشتراک برای اندروید</a>\n\n<a href='t.me/hello/88'>4-برنامه مخصوص اندروید</a>\n\n<a href='t.me/hello/78'>5-آموزش آپدیت و اتصال به بهترین کانفیگ اندروید</a>\n\n<a href='t.me/hello/43'>6-اتصال برای آیفون(IOS+16)</a>\n\n<a href='t.me/hello/87'>7-آموزش آپدیت در FoXray</a>\n\n<a href='t.me/hello/85'>8-اتصال برای آیفون(IOS-16)</a>\n\n<a href='t.me/hello/87'>9-اتصال به بهترین کانفیگ در Fair Vpn</a>\n\n<a href='t.me/hello/79'>10-اتصال برای PC(IOS-16)</a>\n\n@hello", parse_mode = ParseMode.HTML)

@bot.message_handler(func=lambda message: message.text == 'تعرفه ها')
def tutorials(message):
    user_id = message.chat.id
    check = check_user_in_the_channel(user_id)
    if check == False:
        return bot.send_message(user_id, "برای استفاده از رباط عضو کانالمون شو و بعد امتحان کن \n t.me/")
    dir_path = "tarefe"
    file_name = f"tarefe.jpg"
    local_photo_path = os.path.join(dir_path, file_name)
    with open(local_photo_path, 'rb') as photo_to_send:
            bot.send_photo("1199074676", photo_to_send, caption="😱فیلترشکن یکماهه نامحدود 74 T😱\n\n\n\n🎮آیپی ثابت مخصوص ترید و گیم و اسپاتیفای\n\n🛒@\n\n1️⃣پلن یکماهه👀\n\nتک کاربر / 74 T\n2 كاربر / 130 T\n\n 3 کاربر به بالا هم موجود میباشد🔥\n\n🔥 یکماهه Vip😎\n\nتک کاربر / 99 T\n2 کاربر / 158 T\n\n🛒@\n\n3️⃣پلن سه ماهه😎\n\nتک کاربر / 188 T\n2 کاربر / 298 T\n\n🔥 سه ماهه Vip😎\n\nتک کاربر / 248 T\n2 کاربر / 368 T\n\n\n🗺 دسترسی به 8لوکیشن با 1 اشتراک ( آلمان🇩🇪، ترکیه🇹🇷، فنلاند🇫🇮، آمریکا🇺🇸، فرانسه🇫🇷، لهستان🇵🇱، انگلستان🇬🇧، کانادا🇨🇦)\n\n💡 قابل اجرا در: Android, ios, windows\n\n🏆تضمین سرعت و اتصال بدون قطعی\n\n🧑🏼‍💻پشتیبانی و پاسخگویی ۲۴ ساعته\n\n\n🟢با ما خریدی مطمعن و با رضایت داشته باشید 🛍\n\n🛒جهت خرید و مشاوره :\n🏪@hello\n🏪@hello")

@bot.message_handler(func=lambda message: message.text == "🛍خرید برای دیگران")
def purchase_major(message):
    user_id = message.chat.id
    check = check_user_in_the_channel(user_id)
    if check == False:
        return bot.send_message(user_id, "برای استفاده از رباط عضو کانالمون شو و بعد امتحان کن \n t.me/")
    bot.send_message(user_id, "🛍خرید برای دیگران")


@bot.message_handler(func=lambda message: message.text == '⭐️خرید سرویس')
def buy_button(message):
    user_id = message.chat.id
    check = check_user_in_the_channel(user_id)
    if check == False:
        return bot.send_message(user_id, "برای استفاده از رباط عضو کانالمون شو و بعد امتحان کن \n t.me/")
        
    message_tq = "📃 بخشنامه فروش تمامی سرویس های  :\n\n 1- سرویس های مذکور برحسب مصلحت در شرایط با پروتکل های متفاوتی تهیه و تحویل خواهد شد.درصورت نیاز به پروتکل خاص و درخواستی موارد ذیل را قبل از ثبت سفارش به پشتیبانی اطلاع دهید.\n\n2- تمامی سرویس های اعضای قلی خان به جز پلن فمیلی، تک کاربر بوده و فقط و فقط برای یک دستگاه ساخته شده است. درصورت عدم رعایت و وارد کردن اکانت در دستگاه دوم اکانت شما بن شده و از گارانتی ساقط خواهد بود.استفاده همزمان و غیرهمزمان و نوبتی و روزانه و شبانه از هر اکانت در دو دستگاه مطلقاً ممنوع بوده و از دسترس خارج خواهد شد.\n\n3- تمامی اعضای صیانت ضمانت سرعت دانلود ، اپلود را خواهند داشت و  تضمین اتصال شما برعهده ما خواهد بود.\n\n4- گارانتی اکانت شما تماما مربوط به تاریخچه ثبت سفارش شما در ربات می باشد.به هیچوجه تاریخچه چت خود با ربات را پاک نکنید.پیگیری گارانتی اکانت ها صرفا با اکانت تلگرامی که با آن اقدام به خرید کردید میسر خواهد بود.\n\n5- تحویل تمامی سرویس های رفع محدودیت تا ۱۰ دقیقه خواهد بود. پیگیری سفارش قبل از مدت زمان ذکر شده باعث تاخیر در تحویل سفارش شما خواهد شد."

    bot.send_message(user_id, message_tq, reply_markup=inline_keyboard_agreement)


@bot.message_handler(func=lambda message: message.text == '🧪لینک تست')
def test_link(message):
    user_id = message.chat.id
    check = check_user_in_the_channel(user_id)
    if check == False:
        return bot.send_message(user_id, "برای استفاده از رباط عضو کانالمون شو و بعد امتحان کن \n t.me/")
    
    if len(db.get_test_by_user(user_id))==0:
        message_tq = "🟢 لینک تست شما تا پایان امروز برای شما ارسال میگردد"
        message_admin =f"باید لینک تست به آیدی {user_id} ارسال شود"
        test_id = uuid.uuid4().int & (1<<32)-1
        db.insert_test(test_id, user_id)
        bot.send_message(user_id, message_tq)
        bot.send_message('1199074676', message_admin)
    else:
        message_tq = "🔴 شما از لینک تست خود استفاده کرده اید"
        bot.send_message(user_id, message_tq)

@bot.callback_query_handler(func=lambda query: query.data == 'تایید')
def choose_type(query):
    message_buy = "🛒 مدت زمان سرویس خود را برای خرید انتخاب کنید."
    bot.send_message(query.message.chat.id, message_buy, reply_markup=inline_keyboard_product_types)

@bot.callback_query_handler(func=lambda query: query.data in ['1', '2', '3'])
def choose_volume(query):
    message_buy = "🛒 لطفاً یکی از پلن های زیر را برای خرید انتخاب کنید."
    bot.send_message(query.message.chat.id, message_buy, reply_markup=keyboard_duration_types(query.data))

@bot.callback_query_handler(func=lambda query: 'first choice' in query.data)
def choose_user(query):
    choice = re.findall(r"'([^']*)'", query.data)
    message_buy = "🛒 تعداد کاربر های سرویس خود را مشخص کنید."
    bot.send_message(query.message.chat.id, message_buy, reply_markup=keyboard_duration_type_user(choice[0], choice[1]))

# @bot.callback_query_handler(func=lambda query: 'مدل' in query.data)
# def choose_product(query):
#     message_buy = "🛒 لطفاً محصول مورد نظر را برای خرید انتخاب کنید."
#     bot.send_message(query.message.chat.id, message_buy, reply_markup=keyboard_type_products(query.data))

@bot.callback_query_handler(func=lambda query: 'final choice' in query.data)
def invoice(query):
    print(query.data)
    data : str = query.data
    choice = re.findall(r"'([^']*)'", data)
    print(choice)
    duration = choice[0]
    name = choice[1]
    user = choice[2]
    plan_name = 'ساب'
    if name == 'vless':
        plan_name = 'تک لینک'
    if name == 'ssh':
        plan_name = 'S S H'
    volume = "limitless"
    purchase_id = generate_purchase_id()
    user_id = query.message.chat.id
    product = db.get_product_by_name(name)
    not_available = f"کانفیگ های {name} در دسترس تمام شده اند"
    if len(product)==0:
        bot.send_message(query.message.chat.id, ".محصول مورد نظر موجود نیست لطفا محصول دیگری انتخاب کنید یا تا موجود شدن آن صبر کنید .")
        return bot.send_message("6313942217", not_available)
    status = "pending"
    price = db.get_price(duration, volume, user, name)
    date = jdatetime.date.fromgregorian(day=datetime.today().day, month=datetime.today().month, year=datetime.today().year).strftime('%Y-%m-%d')
    invoice_message = f"🧾فاکتور شما\n\n 💶قیمت: {price[0][1]} ریال\n\n 💶پلن: {plan_name}\n\n 💶حجم: نامحدود\n\n 💶مدت زمان: {duration} ماه\n\n 💶تعداد کاربر: {user} کاربره\n\n✅آیا مشخصات بالا مورد تأیید شماست؟"
    
    # insert to database
    db.insert_purchase(purchase_id, user_id, product[0][0], status, date, duration, price[0][1], volume, user, date)
    bot.send_message(user_id, invoice_message, reply_markup=inline_keyboard_invoice)


@bot.callback_query_handler(func=lambda query: query.data == "بله")
def handle_payment(query):
    message_pay = "✅ روش‌ پرداخت خود را انتخاب کنید:"
    bot.send_message(query.message.chat.id, message_pay, reply_markup=inline_keyboard_payment_method)

@bot.callback_query_handler(func=lambda query: query.data == "لغو")
def reset_process(query):
    message_buy = "🛒 لطفاً محصول مورد نظر را برای خرید انتخاب کنید."
    bot.send_message(query.message.chat.id, message_buy, reply_markup=inline_keyboard_product_types)


@bot.callback_query_handler(func=lambda query: query.data == "کیف پول")
def payment_wallet_1(query):
    user = db.get_user_by_id(query.message.chat.id)[0]
    last_purchase = db.get_user_purchase(user[0])
    if len(last_purchase) > 0 and last_purchase[0][3]=="pending":
        price = int(last_purchase[0][6])
        if user[3] >= price:     
            invoice_message = f"🧾پرداخت از کیف پول:\n\n 💶هزینه سرویس: {price} ریال\n\n 💶موجودی حساب شما: {user[3]} ریال\n\n✅آیا مایل به پرداخت نهایی هستید؟"
            bot.send_message(query.message.chat.id, invoice_message, reply_markup=inline_keyboard_final_payment)
        else:
            invoice_message = f"❌موجودی حساب شما کافی نمی باشد\n\n 💶هزینه سرویس: {price} ریال\n\n 💶موجودی حساب شما: {user[3]} ریال"
            bot.send_message(query.message.chat.id, invoice_message, reply_markup=inline_keyboard_user_charge)
    else:
        bot.send_message(query.message.chat.id, "سفارش شما پیدا نشد")


@bot.callback_query_handler(func=lambda query: query.data == "پرداخت نهایی")
def payment_wallet_2(query):
    user = db.get_user_by_id(query.message.chat.id)[0]
    last_purchase = db.get_user_purchase(user[0])
    if len(last_purchase) > 0 and last_purchase[0][3]=="pending":
        price = int(last_purchase[0][6])
        if user[3] >= price:     
            date = jdatetime.date.fromgregorian(day=datetime.today().day, month=datetime.today().month, year=datetime.today().year).strftime('%Y-%m-%d')
            expire = jdatetime.date.fromgregorian(day=datetime.today().day, month=datetime.today().month + last_purchase[0][5], year=datetime.today().year).strftime('%Y-%m-%d')
            amount = user[3]-price
            product_id= db.get_last_purchase_product_id(user[0])
            product = db.get_product_by_id(product_id)[0]
            db.update_purchase_status(last_purchase[0][0])
            db.update_purchase_date(date, expire, last_purchase[0][0])
            db.update_product_status(product_id)
            db.update_user_wallet(amount, user[0])
            message_link = f"خرید شما با موفقیت انجام شد✅ \n\n برای دریافت اطلاعات سرویس خود بر روی دکمه سرویس های من ضربه بزنید 💡 \n\n و برای یادگیری روند اتصال بر روی دکمه راهنما اتصال ضربه بزنید 💡 "
            
            bot.send_message(user[0], message_link)
            admin_message = f'کانفیگ \n \n "{product[3]}" \nباید به مدت {last_purchase[0][5]} ماه به حجم {last_purchase[0][7]} گیگ شارژ شود({last_purchase[0][8]} کاربره)'
            bot.send_message("1199074676", admin_message)
        else:
            bot.send_message(user[0], "🟠موجودی حساب شما کافی نیست", reply_markup=inline_keyboard_user_charge)
        
    else:
        bot.send_message(query.message.chat.id, "خرید شما پیدا نشد")


# @bot.callback_query_handler(func=lambda query: query.data == 'رمز ارز ترون')
# def payment_trx(query):
#     user_id = query.message.chat.id
#     last_purchase = db.get_user_purchase(user_id)
#     if last_purchase is not None:
#         price = int(last_purchase[0][6])
#         if price is not None:
#             link = f"https://changeto.cards/quick/?irrAmount={price}&currency=TRX&address=TEQthXdBL71s786QhtmNaJQ4y9ZebLw9Pz"
#             message_pay_link = f"1️⃣ برای پرداخت به درگاه ریالی وصلد خواهید شد.\n\n2️⃣ بر روی لینک زیر کلیک " \
#                                f"کنید.\n\n3️⃣ لطفاً آموزش را مطالعه بفرمایید. (۳۰ ثانیه از وقت شما رو می‌گیره:)\n\n4️⃣ " \
#                                f"پرداخت شما به صورت امن از طریق درگاه تایید شده خواهد بود و نگرانی‌ای وجود نخواهد " \
#                                f"داشت.\n\n5️⃣ در مرحله آخر اسکرین‌شات پرداخت و فاکتور تایید شده توسط درگاه را ارسال " \
#                                f"بفرمایید.\n\n6️⃣ صبر کنید تا پرداخت شما تایید بشود. (ممکن است ۵ دقیقه الی ۱ ساعت " \
#                                f"زمان ببرد این پروسه)\n\n✅ لینک پرداخت شما:\n{link}"
#             bot.send_message(user_id, message_pay_link, reply_markup=inline_keyboard_trx_tutorial)
#         else:
#             bot.send_message(query.message.chat.id, "The selected product does not have an associated payment link.")
#     else:
#         bot.send_message(query.message.chat.id, "No previous purchases found.")

@bot.callback_query_handler(func=lambda query: query.data == 'کارت به کارت')
def payment_trx(query):
    user_id = query.message.chat.id
    last_purchase = db.get_user_purchase(user_id)
    if len(last_purchase)==1 and last_purchase[0][3]=="pending":
        price = int(last_purchase[0][6])
        message_pay_link = f"1️⃣ لطفا مبلغ {price} ریال را به کارت زیر انتغال دهید \n\n xxxx-xxxx-xxxx-xxxx \n 🪪|به نام: قلی خان \n\n 📃| بعد از واریز مبلغ مورد نظر، عکس رسید تراکنش خود را همینجا ارسال کنید. \n\n(این پیام تا 5 دقیفه حذف خواهد شد)⛔\n\n قلی خان🕊 "
        mess = bot.send_message(user_id, message_pay_link)
        mess_id = mess.message_id
        tim = int(time.time())
        bot.send_message(user_id, tim)
        db.insert_message(mess_id, user_id, tim)
    else:
        bot.send_message(user_id, 'خرید شما پیدا نشد')

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    messagebox = "رسید شما دریافت شد.\nمنتظر بمونید تا پرداخت شما تایید بشه :)\nممنون از صبوریتون."
    user_id = message.from_user.id

    last_purchase = db.get_user_purchase(user_id)
    if len(last_purchase) == 0:
        return bot.send_message(user_id, "سفارش شما پیدا نشد")

    price = last_purchase[0][6]
    last_product_id = last_purchase[0][2]
    photo = message.photo[-1]
    file_path = bot.get_file(photo.file_id).file_path
    downloaded_file = bot.download_file(file_path)

    dir_path = "receipts/img"
    file_name = f"photo_{time.time()}.jpg"
    local_photo_path = os.path.join(dir_path, file_name)

    # Create the directory if it doesn't exist
    os.makedirs(dir_path, exist_ok=True)

    # Save the photo locally
    with open(local_photo_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    caption = f"Price for purchase: {price}, {user_id}"

    admin_payment_verify(local_photo_path, caption, user_id)

    bot.reply_to(message, messagebox)


# def extract_user_id_from_caption(caption):
#     parts = [part.strip() for part in caption.split(',')]
#     user_id = int(parts[1])
#     return user_id


# @bot.channel_post_handler(content_types=['text'])
# def handle_channel_post(message):
#     if "confirm" in message.text.lower() and message.reply_to_message is not None:
#         # Extract the user_id from the caption of the replied-to message
#         user_id = extract_user_id_from_caption(message.reply_to_message.caption)
#         product_id = db.get_last_purchase_product_id(user_id)
#         if users_instance.user_exist(user_id) != "user exist":
#             users_instance.create_user(user_id)
#             users_instance.modify_purchase(user_id, product_id)
#         else:
#             users_instance.modify_purchase(user_id, product_id)
#         link_sub = users_instance.get_link_sub(user_id)
#         print("Photo confirmed")
#         bot.reply_to(message, f"Payment confirmed! Product sent to user {user_id}.")
#         message_link = f"💡با لینک زیر میتونین به سرویس هاتون دسترسی پیدا کنید:\n{link_sub}\n\nاز طریق « راهنما اتصال » " \
#                        f"در منو بات ، روش متصل شدن به سرویس ما رو میتونید یاد بگیرید.\n\nبرای اطلاع از نوع سرویس و باقی " \
#                        f"مانده حساب خود ، روی « 🪪 اطلاعات سرویس » در منو بات کلیک کنید."
#         bot.send_message(user_id, message_link)
#         db.update_purchase_status(user_id)


#admin
@bot.message_handler(func=lambda message: message.text == 'ادمین')
def admin_panel(message):
    if message.from_user.id == 6313942217 or message.from_user.id == 1199074676:
        message_tq = " ادمین تایید شد"
        bot.send_message(message.chat.id, message_tq, reply_markup=inline_keyboard_admin_panel)
    else:
        message_tq = "شما ادمین نیستید"
        bot.send_message(message.chat.id, message_tq)


@bot.callback_query_handler(func=lambda query: query.data == "محصولات")
def admin_products(query):
    available_products = db.get_available_products()
    available_count = len(available_products)
    unavailable_products = db.get_unavailable_products()
    unavailable_count = len(unavailable_products)
    response = f"{available_count} محصول در حال حاضر آزاد و {unavailable_count} محصول در حال استفاده هستند"
    bot.send_message(query.message.chat.id, response, reply_markup=inline_keyboard_admin_products)


@bot.callback_query_handler(func=lambda query: query.data == "اضافه کردن")
def admin_products_add_1(query):
    response = 'add config "plan" "config"'
    bot.send_message(query.message.chat.id, response)


@bot.message_handler(func=lambda message: "add config" in message.text)
def admin_products_add_2(message):
    if message.from_user.id == 6313942217 or message.from_user.id == 1199074676:
        user_id = message.chat.id
        product = re.findall(r'"([^"]*)"', message.text)
        plan = product[0]
        conf = product[1]
        product_id = uuid.uuid4().int & (1<<32)-1
        db.insert_product(product_id, plan, 1, conf, 1, "available", '1')
        bot.send_message(user_id, "محصول با موفقیت اضافه شد")

@bot.callback_query_handler(func=lambda query: query.data == "حذف کردن")
def admin_products_delete_1(query):
    response = 'delete config "conf1", "conf2", "conf3", ...'
    bot.send_message(query.message.chat.id, response)


@bot.message_handler(func=lambda message: "delete config" in message.text)
def admin_products_delete_2(message):
    if message.from_user.id == 6313942217 or message.from_user.id == 1199074676:
        user_id = message.chat.id
        configs = re.findall(r'"([^"]*)"', message.text)

        for conf in configs:
            db.delete_product(conf)
        bot.send_message(user_id, "محصولات با موفقیت حذف شدند")


@bot.callback_query_handler(func=lambda query: query.data == "فروش ها")
def admin_purchases(query):
    confirmed_purchases = db.get_confirmed_purchases()
    confirmed_count = len(confirmed_purchases)
    income = 0
    for purchase in confirmed_purchases:
        income += purchase[6]
    pending_purchases = db.get_pending_purchases()
    pending_count = len(pending_purchases)
    response = f"شما تا کنون {confirmed_count} فروش تایید شده و {pending_count} فروش تایید نشده داشته اید. درآمد کل: {income}"
    bot.send_message(query.message.chat.id, response)


@bot.callback_query_handler(func=lambda query: query.data == "کاربران")
def admin_users(query):
    users = db.get_users()
    count = len(users)
    response = f'شما در حال حاضر {count} کاربر فعال دارید'
    bot.send_message(query.message.chat.id, response, reply_markup=inline_keyboard_admin_users)

@bot.callback_query_handler(func=lambda query: query.data == 'پیام به کاربران')
def admin_users_send_message_1(query):
    response = 'message "your message"'
    bot.send_message(query.message.chat.id, response)

@bot.callback_query_handler(func=lambda query: query.data == 'شارژ کیف پول')
def admin_users_wallet_charge_1(query):
    response = 'charge wallet "user_id" "amount"'
    bot.send_message(query.message.chat.id, response)


@bot.message_handler(func=lambda message: "charge wallet" in message.text)
def admin_users_wallet_charge_2(message):
    user_id = message.from_user.id
    if user_id == 6313942217 or user_id == 1199074676:
        charge = re.findall(r'"([^"]*)"', message.text)
        user = db.get_user_by_id(charge[0])
        if len(user) != 1:
            return bot.send_message(user[0], "کاربر پیدا نشد")
        db.update_user_wallet(charge[1], charge[0])
        bot.send_message(user_id, "کیف پول با موفقیت شارژ شد")
        bot.send_message(charge[0], "کیف پول شما به مبلغ درخواستی شارژ شد✅ \n \n برای دیدن موجودی حساب خود روی دکمه پروفایل ضربه بزنید")



@bot.message_handler(func=lambda message: "message" in message.text)
def admin_users_send_message_2(message):
    if message.from_user.id == 6313942217 or message.from_user.id == 1199074676:
        users = db.get_users()
        send_message = re.findall(r'"([^"]*)"', message.text)
        for user in users:
            bot.send_message(user[0], send_message)
        bot.send_message(message.chat.id, "پیام شما با موفقیت به تمامی کاربران ارسال شد")


@bot.callback_query_handler(func=lambda query: query.data == "قیمت")
def admin_price(query):
    prices = db.get_all_prices()
    response = f'قیمت ها: \n\n'
    for price in prices:
        response += f'تعداد ماه: {price[2]} \nپلن: {price[5]} \n حجم: {price[3]} \n تعداد کاربر: {price[4]} \n قیمت: {price[1]} \n\n\n'
    bot.send_message(query.message.chat.id, response, reply_markup=inline_keyboard_admin_prices)


@bot.callback_query_handler(func=lambda query: query.data == "قیمت جدید")
def admin_price_update(query):
    response = 'price "new price" "months count" "volume" "users" "plan"'
    bot.send_message(query.message.chat.id, response)


@bot.message_handler(func=lambda message: "price" in message.text)
def admin_users_send_message_2(message):
    if message.from_user.id == 6313942217 or message.from_user.id == 1199074676:
        new_price = re.findall(r'"([^"]*)"', message.text)
        price = new_price[0]
        duration = new_price[1]
        volume = new_price[2]
        user = new_price[3]
        plan = new_price[4]
        price_id = uuid.uuid4().int & (1<<32)-1
        
        if len(db.get_price(duration, volume, user, plan))==0:
            db.insert_price(price_id, price, duration, volume, user, plan)
        else:
            db.update_price(price, duration, volume, user, plan)
        bot.send_message(message.chat.id, "قیمت جدید با موفقیت اضافه شد")

@bot.callback_query_handler(func=lambda query: query.data == "لینک تست")
def admin_test_link_1(query):
    response = 'test "user id" "test link"'
    bot.send_message(query.message.chat.id, response)

@bot.message_handler(func=lambda message: "test" in message.text)
def admin_test_link_2(message):
    if message.from_user.id == 6313942217 or message.from_user.id == 1199074676:
        test = re.findall(r'"([^"]*)"', message.text)
        user_id = test[0]
        link = test[1]
        message = f'🔗این اشتراک فقط برای یک روز اعتبار دارد\n\n ✅ لینک مستقیم برای تست سرویس: \n\n {link} 💡'
        bot.send_message(user_id, message)
        bot.send_message(message.chat.id, "لینک تست فرستاده شد")