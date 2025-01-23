import json
from typing import List
from products import Product, get_product
from cart import dao


class Cart:
    def __init__(self, id: int, username: str, contents: List[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data: dict) -> 'Cart':
        return Cart(
            id=data['id'],
            username=data['username'],
            contents=[Product(**item) for item in json.loads(data['contents'])],
            cost=data['cost']
        )


def get_cart(username: str) -> List[Product]:
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    products_list = []
    for cart_detail in cart_details:
        try:
            contents = json.loads(cart_detail['contents'])
            products_list.extend(get_product(product_id) for product_id in contents)
        except (json.JSONDecodeError, KeyError) as e:
            # Log or handle the error as needed
            print(f"Error processing cart contents: {e}")
            continue

    return products_list


def add_to_cart(username: str, product_id: int):
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str):
    dao.delete_cart(username)
