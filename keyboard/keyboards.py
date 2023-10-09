import re
from telebot import types


# the main keyboard
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons_row1 = [
    types.KeyboardButton('⭐️خرید سرویس'),
    types.KeyboardButton('🧪لینک تست'),
]
buttons_row2 = [
    types.KeyboardButton('شارژ حساب 🔗'),
    types.KeyboardButton('🪪 سرویس های من'),
]
buttons_row3 = [
    types.KeyboardButton('سوالات متداول❓'),
    types.KeyboardButton('تعرفه ها'),
    types.KeyboardButton('🪪پروفایل'),
]
buttons_row4 = [
    types.KeyboardButton('💬پشتیبانی'),
    types.KeyboardButton('📚راهنما اتصال'),
]
keyboard.add(*buttons_row1)
keyboard.add(*buttons_row2)
keyboard.add(*buttons_row3)
keyboard.add(*buttons_row4)


# inline keyboard for handle the FAQZ for the buy products and using the bot products
inline_keyboard_agreement = types.InlineKeyboardMarkup(row_width=1)
agree_button = types.InlineKeyboardButton("تایید", callback_data="تایید")
inline_keyboard_agreement.add(agree_button)


# inline keyboard for handle  products
inline_keyboard_products = types.InlineKeyboardMarkup(row_width=1)
product1 = types.InlineKeyboardButton('⚪️ نقره‌ای 1 : یک ماهه 30GB', callback_data='⚪️ نقره‌ای 1 : یک ماهه 30GB')
product2 = types.InlineKeyboardButton('⚪️ نقره‌ای 2 : یک ماهه 50GB', callback_data='⚪️ نقره‌ای 2 : یک ماهه 50GB')
product3 = types.InlineKeyboardButton('🟡 طلایی 1 : یک ماهه 80GB', callback_data='🟡 طلایی 1 : یک ماهه 80GB')
product4 = types.InlineKeyboardButton('🟡 طلایی 2 : یک ماهه 100GB', callback_data='🟡 طلایی 2 : یک ماهه 100GB')
product5 = types.InlineKeyboardButton('🟡 طلایی 3 : یک ماهه 200GB', callback_data='🟡 طلایی 3 : یک ماهه 200GB')
product6 = types.InlineKeyboardButton('🟠 پلاتینیوم 1 : سه ماهه 80GB', callback_data='🟠 پلاتینیوم 1 : سه ماهه 80GB')
product7 = types.InlineKeyboardButton('🟠 پلاتینیوم 2 : سه ماهه 100GB', callback_data='🟠 پلاتینیوم 2 : سه ماهه 100GB')
product8 = types.InlineKeyboardButton('🟠 پلاتینیوم 3 سه ماهه 250 GB', callback_data='🟠 پلاتینیوم 3 سه ماهه 250 GB')
inline_keyboard_products.add(product1, product2, product3, product4, product5, product6, product7, product8)


# inline keyboard for handle  product types
inline_keyboard_product_types = types.InlineKeyboardMarkup(row_width=1)
type1 = types.InlineKeyboardButton('1️⃣ ماهه', callback_data=1)
type2 = types.InlineKeyboardButton('2️⃣ ماهه', callback_data=2)
type3 = types.InlineKeyboardButton('3️⃣ ماهه', callback_data=3)
inline_keyboard_product_types.add(type1, type2, type3)

# inline keyboard for charging
inline_keyboard_user_charge = types.InlineKeyboardMarkup(row_width=1)
ty1 = types.InlineKeyboardButton('شارژ حساب', callback_data="شارژ حساب")
ty2 = types.InlineKeyboardButton('کارت به کارت', callback_data="کارت به کارت")
inline_keyboard_user_charge.add(ty1, ty2)

def keyboard_duration_types(duration):
    keyboard_duration_volumes = types.InlineKeyboardMarkup(row_width=2)
    prod1 = types.InlineKeyboardButton('نامحدود♾️ ساب(800 سرور)', callback_data=f"first choice '{duration}' 'sub'")
    prod2 = types.InlineKeyboardButton('نامحدود♾️ تک لینک(Vless)', callback_data=f"first choice '{duration}' 'vless'")
    prod3 = types.InlineKeyboardButton('نامحدود♾️ SSH', callback_data=f"first choice '{duration}' 'ssh'")
    keyboard_duration_volumes.add(prod1, prod2, prod3)
    return keyboard_duration_volumes

def keyboard_duration_type_user(duration, type):
    keyboard_duration_volume_user = types.InlineKeyboardMarkup(row_width=2)
    u1 = types.InlineKeyboardButton("1 کاربره", callback_data=f"final choice '{duration}' '{type}' '1'")
    u2 = types.InlineKeyboardButton("2 کاربره", callback_data=f"final choice '{duration}' '{type}' '2'")
    keyboard_duration_volume_user.add(u1, u2)
    return keyboard_duration_volume_user
# inline keyboard for handle user invoice
inline_keyboard_invoice = types.InlineKeyboardMarkup(row_width=1)
yes_btn = types.InlineKeyboardButton("بله", callback_data="بله")
no_btn = types.InlineKeyboardButton("لغو", callback_data="لغو")
inline_keyboard_invoice.add(yes_btn, no_btn)

# inline keyboard for handle user extend
def keyboard_user_extend(purchase_id):
    inline_keyboard_user_extend = types.InlineKeyboardMarkup(row_width=1)
    extend = types.InlineKeyboardButton("تمدید", callback_data=f"تمدید '{purchase_id}'")
    inline_keyboard_user_extend.add(extend)
    return inline_keyboard_user_extend

# inline keyboard for handle payment method
inline_keyboard_payment_method = types.InlineKeyboardMarkup(row_width=1)
crypto = types.InlineKeyboardButton("✅کارت به کارت✅", callback_data="کارت به کارت")
perfect_money = types.InlineKeyboardButton("✅کیف پول✅", callback_data="کیف پول")
inline_keyboard_payment_method.add(
    crypto, 
    perfect_money, 
    # cart_to_cart
)

# inline keyboard for handle tutorials
inline_keyboard_tutorials = types.InlineKeyboardMarkup(row_width=1)
iphone = types.InlineKeyboardButton("مک و آیفون", callback_data="مک و آيفون", url="https://t.me/QiTutorialz/121")
android = types.InlineKeyboardButton("اندروید و ویندوز", callback_data="اندروید و ویندوز",
                                     url="https://t.me/QiTutorialz/66")
inline_keyboard_tutorials.add(iphone, android)
inline_keyboard_trx_tutorial = types.InlineKeyboardMarkup(row_width=1)
tutorial = types.InlineKeyboardButton("نحوه پرداخت", callback_data="نحوه پرداخت", url="https://t.me/QiPaymentz/22")
inline_keyboard_trx_tutorial.add(tutorial)

# inline keyboard for final payment
inline_keyboard_final_payment = types.InlineKeyboardMarkup(row_width=1)
b4 = types.InlineKeyboardButton('پرداخت نهایی', callback_data='پرداخت نهایی')
inline_keyboard_final_payment.add(b4)



# inline keyboard for admin panel
inline_keyboard_admin_panel = types.InlineKeyboardMarkup(row_width=1)
b1 = types.InlineKeyboardButton('محصولات', callback_data='محصولات')
b2 = types.InlineKeyboardButton('فروش ها', callback_data='فروش ها')
b3 = types.InlineKeyboardButton('قیمت', callback_data='قیمت')
b4 = types.InlineKeyboardButton('کاربران', callback_data='کاربران')
b5 = types.InlineKeyboardButton('لینک تست', callback_data='لینک تست')
inline_keyboard_admin_panel.add(b1, b2, b3, b4, b5)

# inline keyboard for admin products
inline_keyboard_admin_products = types.InlineKeyboardMarkup(row_width=1)
f1 = types.InlineKeyboardButton('اضافه کردن', callback_data='اضافه کردن')
f2 = types.InlineKeyboardButton('حذف کردن', callback_data='حذف کردن')
inline_keyboard_admin_products.add(f1, f2)

# inline keyboard for admin users
inline_keyboard_admin_users = types.InlineKeyboardMarkup(row_width=1)
z1 = types.InlineKeyboardButton('پیام به کاربران', callback_data='پیام به کاربران')
z2 = types.InlineKeyboardButton('شارژ کیف پول', callback_data='شارژ کیف پول')
inline_keyboard_admin_users.add(z1, z2)

# inline keyboard for admin prices
inline_keyboard_admin_prices = types.InlineKeyboardMarkup(row_width=1)
g1 = types.InlineKeyboardButton('قیمت جدید', callback_data='قیمت جدید')
inline_keyboard_admin_prices.add(g1)