
from src.Helper.order_helper import OrderHelper
import pytest
from src.Utilities.wooAPIUtility import wooAPIUtility
from src.Helper.coupon_helper import CouponHelper
from src.Helper.product_helper import ProductHelper
from src.Utilities import GenericUtilities
import random



pytestmark = [pytest.mark.order, pytest.mark.coupon, pytest.mark.regression]
@pytest.mark.TCID60
def test_order_with_50per_coupon():
    order_helper = OrderHelper()
    coupon_helper= CouponHelper()
    product_helper = ProductHelper()


    #create coupon with 50% off
    coupon_payload = { "code": "newseason",
    "discount_type": "percent",
    "amount": "50",
    "individual_use": True,
    "exclude_sale_items": True}

    # coupon_info = coupon_helper.call_create_coupon(coupon_payload)
    # coupon_id = coupon_info['id']




    #create a product with noted price
    regular_price = str(random.randint(10,100))+'.'+str(random.randint(10,99))
    Product_payload=dict()
    Product_payload['name'] = GenericUtilities.generate_random_string(5)
    Product_payload['type'] = 'simple'
    Product_payload['regular_price'] = regular_price
    product_info = product_helper.call_create_product(Product_payload)
    product_id = product_info['id']


    #create the order and verify
    order_payload=dict()
    order_payload={
    "coupon_lines":[{"code":coupon_payload['code']}],
    "line_items":[{"product_id":product_id,"quantity": 1}]
    }
    order_info = order_helper.call_create_order(order_payload)

    expected_total = round(float(regular_price)*int(coupon_payload['amount'])/100,2)
    total = round(float(order_info['total']),2)

    assert expected_total==total, f"expected_total doesn't take the coupon percentage off, expected:{expected_total},actual:{total}"


