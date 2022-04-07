
import pytest
from src.DataAccessObject.Products_dao import ProductDAO
from src.DataAccessObject.Orders_dao import OrdersDAO
from src.Helper.order_helper import OrderHelper
from src.Helper.customer_helper import CustomerHelper


@pytest.fixture(scope='module')
def my_orders_smoke_setup():
    product_dao = ProductDAO()
    rand_product = product_dao.get_random_product_from_db(1)
    product_id = rand_product[0]['ID']
    order_help = OrderHelper()
    info = {'product_id':product_id,
            'order_help':order_help}


    return info


@pytest.mark.TCID48
@pytest.mark.orders
@pytest.mark.smoke
def test_create_paid_order_guest_user(my_orders_smoke_setup):

    order_help = my_orders_smoke_setup['order_help']

    customer_id = 0
    product_id = my_orders_smoke_setup['product_id']
    #get a product from DB


    #make the call - helper make the calls
    info = {"line_items": [
            {
                "product_id": product_id, 
                "quantity": 1
            }
            ]}
    order_json = order_help.create_order(additioanl_args=info)

    expected_products = [{'product_id':product_id}]
    order_help.verify_order_is_created(order_json,customer_id,expected_products)
    #order_help.verify_order_is_created()
    # #verify response
    # assert order_json, f"create order response is empty"
    # assert order_json['customer_id'] == customer_id, f"Create order as guest expected default customer_id = 0"\
    #     f", but got {order_json['customer_id']}"
    # assert len(order_json['line_items']) == 1, f"expected only 1 item in order but found{len(order_json['line_items'])}"\
    #     f"Order id is :{order_json['id']}"


    # #verify DB
    # order_id = order_json['id']
    # line_info = Order_dao.get_order_lines_by_id(order_id)
    # assert line_info, f"Create order, line item not found in DB. Order ID: {order_id}"
    

    # line_items = [i for i in line_info if i ['order_item_type']=='line_item']
    # assert len(line_items) ==1 , f"expected 1 line item but found {len(line_items)}. Order id is: {order_id}"
    
    # line_id = line_items[0]['order_item_id']
    # line_details = Order_dao.get_order_items_details(line_id)

    # db_product_id = line_details['_product_id']
    # assert str(db_product_id) == str(product_id), f"Create order 'product id' in db does not match in API."\
    #     f"API product id is: {product_id}, DB product id is: {db_product_id}"













@pytest.mark.TCID49
@pytest.mark.orders
@pytest.mark.smoke
def test_create_paid_order_new_created_customer(my_orders_smoke_setup):
    #create helper objects
    customer_helper = CustomerHelper()


    #get a product from DB



    #make the call - helper make the calls
    cust_info = customer_helper.create_customer()
    customer_id = cust_info['id']
    product_id = my_orders_smoke_setup['product_id']
    order_help = my_orders_smoke_setup['order_help']

    info = {"line_items": [
            {
                "product_id": product_id,
                "quantity": 1
            }
            ],
            "customer_id":customer_id}
    order_json = order_help.create_order(additioanl_args=info)


    expected_products = [{'product_id':product_id}]
    order_help.verify_order_is_created(order_json,customer_id,expected_products)
    # #verify response
    # assert order_json, f"create order response is empty"
    # assert order_json['customer_id'] == customer_id, f"Create order with given customer id returned bad customer id"\
    #     f", expected customer_id = {customer_id}, but got {order_json['customer_id']}"
    # import pdb; pdb.set_trace();
    # assert len(order_json['line_items']) == 1, f"expected only 1 item in order but found{len(order_json['line_items'])}"\
    #     f"Order id is :{order_json['id']}"


    # #verify DB
    # order_id = order_json['id']
    # line_info = Order_dao.get_order_lines_by_id(order_id)
    # assert line_info, f"Create order, line item not found in DB. Order ID: {order_id}"
    

    # line_items = [i for i in line_info if i ['order_item_type']=='line_item']
    # assert len(line_items) ==1 , f"expected 1 line item but found {len(line_items)}. Order id is: {order_id}"
    
    # line_id = line_items[0]['order_item_id']
    # line_details = Order_dao.get_order_items_details(line_id)

    # db_product_id = line_details['_product_id']
    # assert str(db_product_id) == str(product_id), f"Create order 'product id' in db does not match in API."\
    #     f"API product id is: {product_id}, DB product id is: {db_product_id}"
