
import os
import json
from src.Utilities.wooAPIUtility import wooAPIUtility
from src.DataAccessObject.Orders_dao import OrdersDAO
from src.Utilities.RequestsUtility import RequestsUtility


class OrderHelper(object):


    def __init__(self):
        #how to get the path of current file in python - Google
        self.cur_file_dir = os.path.dirname(os.path.realpath(__file__))
        self.woo_helper = wooAPIUtility()
        self.requests_utility = RequestsUtility()

    def create_order(self, additioanl_args=None):
        

        payload_template = os.path.join(self.cur_file_dir,'..','data','create_order_payload.json')

        with open(payload_template) as f:
            payload = json.load(f)


            #if user adds more info to payload , then updated
        if additioanl_args:
            assert isinstance(additioanl_args, dict), f"parameter 'additional_args' must be a dictionary but found {type(additioanl_args)}"
            payload.update(additioanl_args)
        
        rs_api = self.woo_helper.post('orders',params=payload,expected_status_code=201)
        
        
        return rs_api


    @staticmethod
    def verify_order_is_created( order_json, exp_cust_id, exp_products):

        Order_dao = OrdersDAO()
        #verify response
        assert order_json, f"create order response is empty"
        assert order_json['customer_id'] == exp_cust_id, f"Create order with given customer id returned bad customer id"\
            f", expected customer_id = {exp_cust_id}, but got {order_json['customer_id']}"
        
        assert len(order_json['line_items']) == len(exp_products), f"expected only {len(exp_products)} item in order but found{len(order_json['line_items'])}"\
            f"Order id is :{order_json['id']}"


        #verify DB
        order_id = order_json['id']
        line_info = Order_dao.get_order_lines_by_id(order_id)
        assert line_info, f"Create order, line item not found in DB. Order ID: {order_id}"
        

        line_items = [i for i in line_info if i ['order_item_type']=='line_item']
        assert len(line_items) ==1 , f"expected 1 line item but found {len(line_items)}. Order id is: {order_id}"
        
        # get list of product ids in the response
        api_product_ids = [i['product_id'] for i in order_json['line_items']]

        for product in exp_products:
            assert product['product_id'] in api_product_ids, f"Create order does not have at least 1 expected product in DB."\
            f"Product_id:{product['product_id']}. Order id: {order_id}"



    def call_update_an_order(self, order_id, payload):
        return self.woo_helper.put(f'orders/{order_id}',params = payload)

    def call_retrieve_an_order(self, order_id):
        return self.woo_helper.get(f"orders/{order_id}")

    def call_create_order(self,payload):
        return self.requests_utility.post('orders',payload=payload,expected_status_code=201)