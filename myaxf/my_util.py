import uuid
import hashlib


#生成唯一验证码
def get_uuid_str():
    uuid_avl = uuid.uuid4()
    uuid_str = str(uuid_avl).encode("utf-8")
    md5 = hashlib.md5()
    md5.update(uuid_str)

    return md5.hexdigest()


#算钱
def get_cart_money(cart_items):
    sum_money = 0
    cart_items = cart_items.filter(
        is_selected = True
    )
    for i in cart_items:
        sum_money += i.goods.price * i.num

    return sum_money
