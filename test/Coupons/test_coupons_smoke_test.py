import pytest
from src.Utilities.wooAPIUtility import wooAPIUtility
from src.Helper.coupon_helper import CouponHelper
from src.Utilities import GenericUtilities
import random

pytestmark = [pytest.mark.regression, pytest.mark.coupons]

@pytest.fixture(scope='module')
def my_setup():
    info = {}
    info['coupon_helper'] = CouponHelper()

    return info

@pytest.mark.parametrize('discount_type',
[
pytest.param(None,marks=[pytest.mark.TCID36, pytest.mark.smoke]),
pytest.param('percent',marks=[pytest.mark.TCID37, pytest.mark.smoke]),
pytest.param('fixed_product',marks=[pytest.mark.TCID38, pytest.mark.smoke]),
pytest.param('fixed_cart',marks=[pytest.mark.TCID39, pytest.mark.smoke]),
])

def test_crete_coupon_percent_discount_type(my_setup,discount_type):
    #decide which discount type to use
    expected_discount_type = discount_type if discount_type else 'discount_cart'

    #set percent off and coupon_code
    pct_off = str(random.randint(50,90)) + '.00' #string
    coupon_code = GenericUtilities.generate_random_string(4,suffix='TCID37')

    #get the helper object
    coupon_helper = my_setup['coupon_helper']

    #payload
    payload = {}
    payload['code']= coupon_code
    payload['amount'] = pct_off

    if discount_type:
        payload['discount_type'] = discount_type
    rs_coupon = coupon_helper.call_create_coupon(payload=payload)
    coupon_id = rs_coupon['id']

    import pdb; pdb.set_trace()

    rs_coupon_2 = coupon_helper.call_retrieve_coupon(coupon_id)

    #assertion
    assert rs_coupon_2['amount'] == pct_off
    assert rs_coupon_2['code'].lower() == coupon_code
    assert rs_coupon_2['discount_type'] == expected_discount_type

