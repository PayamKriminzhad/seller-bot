from handlers.bot_handler import bot, db
import schedule
import time
import jdatetime
from datetime import datetime
from threading import Thread

def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)

def manage_expired_purchases():
    purchases = db.get_confirmed_purchases()
    for purchase in purchases:
        date_str = purchase[9]
        expire = datetime.strptime(date_str, '%Y-%m-%d').date()
        today = jdatetime.date.fromgregorian(year=datetime.today().year,month=datetime.today().month,day=datetime.today().day)
        expire = datetime(expire.year, expire.month, expire.day)
        today = datetime(today.year, today.month, today.day)
        if today > expire:
            db.update_purchase_status_to_expired(purchase[0])

def delete_messages():
    messages = db.get_messages()
    t = int(time.time())
    for m in messages:
        x = t - m[2]
        if x > 300:
            bot.delete_message(m[1], m[0])
            db.remove_message(m[0], m[1])
db.connect()
db.create_tables()
db.disconnect()
if __name__ == '__main__':
    schedule.every().day.do(manage_expired_purchases)
    schedule.every().minute.do(delete_messages)
    Thread(target=schedule_checker).start()
    bot.infinity_polling()


