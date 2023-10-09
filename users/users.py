import datetime
import requests
import uuid


# for handle users traffic limit
def convert_bytes_to_megabytes(bytes_value):
    if bytes_value is None:
        return None
    megabytes = bytes_value / 1024 / 1024
    return f"{megabytes:.2f}"


# class for handle the API requests
class Users:
    # product ids are static in my bot
    PRODUCT_DETAILS = {
        1: (30, 32212254720),
        2: (30, 53687091200),
        3: (30, 85899345920),
        4: (30, 107374182400),
        5: (30, 214748364800),
        6: (90, 85899345920),
        7: (90, 107374182400),
        8: (90, 268435456000)
    }

    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = 'https://marzbanadmin.justadmins.xyz/api/user'
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }

    # this method creates a user in Marzban panel with a custom traffic limit and time
    def create_user(self, user_id):
        now = datetime.datetime.now()
        expire = now + datetime.timedelta(days=1)
        expire_seconds = int(expire.timestamp())
        data = {
            "username": f"{user_id}",
            "proxies": {
                "vmess": {
                    "id": str(uuid.uuid4())
                },
                "vless": {}
            },
            "inbounds": {
                "vmess": [
                    "vmess-ws-http"
                ],
                "vless": [
                    "VLESS TCP REALITY"
                ]
            },
            "expire": expire_seconds,
            "data_limit": 104857600,
            "data_limit_reset_strategy": "no_reset"
        }
        response = requests.post(self.base_url, headers=self.headers, json=data)
        if response.status_code == 200:
            response_data = response.json()
            print("User created successfully.")
        else:
            print("Error:", response.status_code)
            print("Response Body:", response.text)

    # check user existent in panel
    def user_exist(self, user_id):

        url = f"{self.base_url}/{user_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            print("user exist")
            return "user exist"

    # get subscription info for user and pass the data to bot
    def get_user_info(self, user_id):
        url = f"{self.base_url}/{user_id}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            data = response.json()
            user_info = {
                "status": data.get("status"),
                "username": data.get("username"),
                "expire": data.get("expire"),
                "data_limit": convert_bytes_to_megabytes(data.get("data_limit")),
                "used_traffic": convert_bytes_to_megabytes(data.get("used_traffic")),
            }
            key_mapping = {
                "status": "🚥وضعیت",
                "username": "🪪شماره کاربری",
                "expire": "⏰زمان باقی مانده",
                "data_limit": "🔋حجم کل(MB)",
                "used_traffic": "📦حجم استفاده شده(MB)",
            }

            formatted_str = ""
            for key, value in user_info.items():
                if key in key_mapping:
                    formatted_str += f"{key_mapping[key]}: {value} \n"

            print(formatted_str)
            return formatted_str
        elif response.status_code == 404:
            return "User not found"
        else:
            return "Error: " + str(response.status_code)

    def get_link_sub(self, user_id):
        url = f"{self.base_url}/{user_id}"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            data = response.json()
            if "subscription_url" in data:
                sub_link = data["subscription_url"]
                return sub_link

            else:
                return "Subscription URL not found"
        elif response.status_code == 404:
            return "User not found"
        else:
            return "Error: " + str(response.status_code)

    # modify the subscription for user when payment is complete
    def modify_purchase(self, user_id, product_id):
        url = f"{self.base_url}/{user_id}"
        now = datetime.datetime.now()

        data = {
            "username": f"{user_id}",
            "proxies": {
                "vmess": {
                    "id": str(uuid.uuid4())
                },
                "vless": {}
            },
            "inbounds": {
                "vmess": [
                    "vmess-ws-http"
                ],
                "vless": [
                    "VLESS TCP REALITY"
                ]
            },
        }

        if product_id in self.PRODUCT_DETAILS:
            days, data_limit = self.PRODUCT_DETAILS[product_id]
            expire = now + datetime.timedelta(days=days)
            data["expire"] = int(expire.timestamp())
            data["data_limit"] = data_limit
        else:
            raise ValueError(f"Invalid product_id: {product_id}")
        print(f"Product details: {self.PRODUCT_DETAILS}")

        response = requests.put(url, headers=self.headers, json=data)

        return response.json()
