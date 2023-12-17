import requests
import json
base = "https://api.torn.com/market/"
torn_store_base = "https://www.torn.com/imarket.php#/p=shop&step=shop&type=&searchname="
bazaar_ending = "?selections=bazaar&key="
market_ending = "?selections=itemmarket&key="
torn_items = "https://api.torn.com/torn/?selections=items&key="

BAZAAR_INDEX = 0
MARKET_INDEX = 1

class User(dict):
    def __init__(self, key):
        if type(key) is dict:
            self.key = str(key["key"])
            self.item_dict = dict(key["item_dict"])
        else:
            self.key = key
            self.item_dict = {}
            dict.__init__(self, key=key, item_dict=self.item_dict)
        
    def __repr__(self):
        return f"{self.key} {self.item_dict}" 
    
    def get_request_urls(self, id: int):
        item_str = str(id)
        return (base + item_str + bazaar_ending + self.key, base + item_str + market_ending + self.key)
    #Checks all the items in the items_dict, if any has 
    def check_items(self):
        message = ""
        torn_item_dict = requests.get(torn_items + self.key).json()["items"]
        for id, threshold in self.item_dict.items():
            urls = self.get_request_urls(id)
            temp_list = []
            temp_list += requests.get(urls[BAZAAR_INDEX]).json()["bazaar"]
            temp_list += requests.get(urls[MARKET_INDEX]).json()["itemmarket"]
            for listing_info in temp_list:
                if listing_info["cost"] <= threshold:
                    item_name = torn_item_dict[str(id)]["name"]
                    cost = listing_info["cost"]
                    quantity = listing_info["quantity"]
                    message += (f"{item_name}: ${cost:,} x{quantity:,} = ${cost*quantity:,}\n")
                    message += (torn_store_base + item_name.replace(" ", "+") + "\n")
                    break
        return message

    #Maybe unnecessary tbh
    def update_threshold(self, item_id: int, threshold: int):
        self.item_dict[item_id] = threshold

    #Maybe unnecessary tbh
    def check_added(self, item_id: int) -> bool:
        return item_id in self.item_dict
    
    def remove(self, id):
        del self.item_dict[id]

    def list_items(self):
        return "".join([f"{key}\t ${value:,}\n" for key, value in self.item_dict.items()])
def test():
    tst_user = User("L1ZLIuYKllusUNts")
    tst_user.item_dict[367] = 13_800_000
    tst_user.item_dict[283] = 24_000_000
    #print(tst_user.check_items())
    print(tst_user.list_items())
    dump = json.dumps(tst_user) 
    print(json.dumps(tst_user), type(dump))
    loaded = json.loads(dump)
    print(loaded, type(loaded))
    reconstructed = User(loaded)
    print(reconstructed, type(reconstructed))


if __name__ == "__main__":
    test()