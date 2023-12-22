import requests
from copy import deepcopy
base = "https://api.torn.com/market/"
torn_store_base = "https://www.torn.com/imarket.php#/p=shop&step=shop&type=&searchname="
bazaar_ending = "?selections=bazaar&key="
market_ending = "?selections=itemmarket&key="
torn_items_page = "https://api.torn.com/torn/?selections=items&key="

BAZAAR_INDEX = 0
MARKET_INDEX = 1

class User():
    def __init__(self, key):
        if type(key) is dict:
            self.key = str(key["key"])
            self.items = dict(key["items"])
        else:
            self.key = key
            self.items = {}
        
    def __repr__(self):
        return f"{self.key} {self.items}" 
    
    def asdict(self):
        return {"key": self.key, "items": deepcopy(self.items)}
    
    def get_request_urls(self, id: int):
        item_str = str(id)
        return (base + item_str + bazaar_ending + self.key, base + item_str + market_ending + self.key)
    
    #Checks all the items in the items_dict, if any has 
    def check_items(self) -> str:
        torn_items = requests.get(torn_items_page + self.key).json()["items"]
        for id, threshold in self.items.items():
            urls = self.get_request_urls(id)
            temp_list = []
            temp_list += requests.get(urls[BAZAAR_INDEX]).json()["bazaar"]
            temp_list += requests.get(urls[MARKET_INDEX]).json()["itemmarket"]
            message = validate_torn_listings(temp_list, id, threshold, torn_items)
        return message

    def add_item(self, item_id: int, threshold: int):
        """Adds an item to the items dict for tracking
        :Parameters:
            -`item_id`: the id of the item to add
            -`threshold`: cost below which user will be notified """
        self.update_threshold(item_id, threshold)


    def update_threshold(self, item_id: int, threshold: int):
        """Updates a threshold for a given item
        
        :Parameters:
            -`item_id`: the id of the item to add
            -`threshold`: is cost below which user will be notified """
        self.items[item_id] = threshold

    
    def check_added(self, item_id: int) -> bool:
        """Checks if an item has been added to the items dict
        
        :Parameters:
            -`item_id`: the id of the item to check"""
        return item_id in self.items
    
   
    def remove(self, id):
        """Removes an item from items dict given its id
        
        :Parameters:
            -`id`: the id of the item to remove
        """
        del self.items[id]

    def list_items(self) -> str:
        """Returns a string that lists the items added to the items dict"""
        return "".join([f"{key}\t ${value:,}\n" for key, value in self.items.items()])

def validate_torn_listings(item_list,item_id, threshold, torn_items) -> str:
        """Retuns a string contaning the torn store page and the price of a specific item if
        its cost is below the threshold
        
        :Parameters:
            -`item_list`: the list of the market listings for this item
            -`item_id`: the id of the item
            -`thresholdt`: the threshold to check against the market cost 
            -`torn_items`: the dict containing the torn_items JSON info"""
        message = ""
        for listing_info in item_list:
                if listing_info["cost"] <= threshold:
                    item_name = torn_items[str(item_id)]["name"]
                    cost = listing_info["cost"]
                    quantity = listing_info["quantity"]
                    message += (f"{item_name}: ${cost:,} x{quantity:,} = ${cost*quantity:,}\n")
                    message += (torn_store_base + item_name.replace(" ", "+") + "\n")
                    return message


def test():
    tst_user = User("L1ZLIuYKllusUNts")
    tst_user.items[367] = 13_800_000
    tst_user.items[283] = 24_000_000
    print(tst_user.list_items())
    print(tst_user.check_items())


if __name__ == "__main__":
    test()