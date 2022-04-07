
from src.Helper.order_helper import OrderHelper
import pytest
from src.Utilities.wooAPIUtility import wooAPIUtility
from src.Utilities.GenericUtilities import generate_random_string

pytestmark = [pytest.mark.orders, pytest.mark.regression]


##@pytest.mark.order
##@pytest.mark.TCID55
@pytest.mark.parametrize("new_status",
    [pytest.param('cancelled',marks=[pytest.mark.TCID55, pytest.mark.smoke]),
    pytest.param('completed',marks=pytest.mark.TCID56),
    pytest.param('on-hold',marks=pytest.mark.TCID57)
    ])
def test_update_order_status(new_status):
    
    # new_status = 'completed'
    # create new order 
    orderhelper = OrderHelper()
    order_json = orderhelper.create_order()


    # get the current status of the order
    cur_status = order_json['status']
    assert cur_status != new_status, f"curret status of order is already {new_status}."\
        f"Unable to run test."
 

    # update the status
    payload = {"status":new_status}
    order_id = order_json['id']
    orderhelper.call_update_an_order(order_id,payload)
    #make sure busted/refresh cached



    # get order information
    new_order_info = orderhelper.call_retrieve_an_order(order_id)

    # verify the new order status is what was updated
    assert new_order_info['status'] == new_status, f"Updated order status to {new_status}, but order is still"\
        f"{new_order_info['status']}"


@pytest.mark.TCID58
def test_update_order_status_to_random_string():
    new_status = 'abcdefg'
    # create new order 
    orderhelper = OrderHelper()
    order_json = orderhelper.create_order()
    order_id = order_json['id']
    
    # update the status
    payload = {"status":new_status}
    rs_api = wooAPIUtility().put(f'orders/{order_id}',params = payload, expected_status_code = 400)

    assert rs_api['code'] == 'rest_invalid_param', f"Update order status to random string did not have"\
        f"correct code in response. Expected:'rest_invalid_param'. Actual:{rs_api['code']} "

    assert rs_api['message'] == 'Invalid parameter(s): status', f"Update order status to random string did not have"\
        f"correct message in response. Expected:'rest_invalid_param'. Actual:{rs_api['message']} "


@pytest.mark.TCID59
def test_update_order_customer_note():
        # create new order 
    orderhelper = OrderHelper()
    order_json = orderhelper.create_order()
    order_id = order_json['id']

    #update the order
    rand_string = generate_random_string(40)
    payload = {"customer_note":rand_string}
    orderhelper.call_update_an_order(order_id,payload)

    # get order information
    new_order_info = orderhelper.call_retrieve_an_order(order_id)
    assert new_order_info['customer_note'] == rand_string, f"Update order's customer note failed. Expected: {rand_string}. Actual:{new_order_info['customer_note']} "