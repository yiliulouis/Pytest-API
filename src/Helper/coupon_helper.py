from src.Utilities.GenericUtilities import generate_random_email_and_password
from src.Utilities.RequestsUtility import RequestsUtility
from src.Utilities.wooAPIUtility import wooAPIUtility
import logging as logger



class CouponHelper(object):
    def __init__(self):
        self.wooAPIUtility = wooAPIUtility()

    def call_create_coupon(self,payload):
        return self.wooAPIUtility.post('coupons',payload=payload,expected_status_code=201)

    def call_retrieve_coupon(self,coupon_id):
        return self.wooAPIUtility.get(f'coupons/{coupon_id}')