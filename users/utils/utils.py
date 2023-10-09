import requests
import uuid
from datetime import datetime


def get_access_token():
    url = "https://marzbanadmin.justadmins.xyz/api/admin/token"
    data = {
        "grant_type": "password",
        "username": "QiAdmin",
        "password": "Qi@s1383.83",
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        data = response.json()
        access_token = data["access_token"]
        print("access_token:", access_token)
        return str(access_token)

    else:
        print("Error:", response.status_code)


def convert_bytes_to_megabytes(bytes_value):
    if bytes_value is None:
        return None
    megabytes = bytes_value / 1024 / 1024
    return f"{megabytes:.2f}"


def generate_purchase_id():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = uuid.uuid4()
    return f"{timestamp}-{str(unique_id)}"


class OrderIDGenerator:
    current_id = 0

    @classmethod
    def generate_order_id(cls):
        cls.current_id += 1
        return f"order-{cls.current_id}"


product_ids = {
    "product_1": 1,
    "product_2": 2,
    "product_3": 3,
    "product_4": 4,
    "product_5": 5,
    "product_6": 6,
    "product_7": 7,
    "product_8": 8,
}

price_link_map = {
    750000: "https://changeto.cards/quick/?irrAmount=750000&currency=TRX&address=TV8Mw2YG1moD6C2K225L6qmCDDWDHf8XVG",
    1150000: "https://changeto.cards/quick/?irrAmount=1050000&currency=TRX&address=TV8Mw2YG1moD6C2K225L6qmCDDWDHf8XVG",
    1400000: "https://changeto.cards/quick/?irrAmount=1400000&currency=TRX&address=TV8Mw2YG1moD6C2K225L6qmCDDWDHf8XVG",
    1550000: "https://changeto.cards/quick/?irrAmount=1550000&currency=TRX&address=TV8Mw2YG1moD6C2K225L6qmCDDWDHf8XVG",
    2100000: "https://changeto.cards/quick/?irrAmount=2100000&currency=TRX&address=TV8Mw2YG1moD6C2K225L6qmCDDWDHf8XVG",
    2500000: "https://changeto.cards/quick/?irrAmount=2500000&currency=TRX&address=TV8Mw2YG1moD6C2K225L6qmCDDWDHf8XVG",
    3100000: "https://changeto.cards/quick/?irrAmount=3100000&currency=TRX&address=TV8Mw2YG1moD6C2K225L6qmCDDWDHf8XVG",
    4500000: "https://changeto.cards/quick/?irrAmount=4500000&currency=TRX&address=TV8Mw2YG1moD6C2K225L6qmCDDWDHf8XVG",
}


products = [
    [1, "product_1", 750000, 'مدل عادی', "یک ماهه"],
    [2, "product_2", 1150000, 'مدل عادی', "دو ماهه"],
    [3, "product_3", 1400000, 'مدل عادی', "سه ماهه"],
    [4, "product_4", 1550000, 'مدل پرایم', "یک ماهه"],
    [5, "product_5", 2100000, 'مدل پرایم', "دو ماهه"],
    [6, "product_6", 2500000, 'مدل پرایم', "سه ماهه"],
    [7, "product_7", 3100000, 'مدل پرایم بیزینس', 'یک ماهه'],
    [8, "product_8", 4500000, 'مدل پرایم بیزینس', 'دو ماهه'],
]
