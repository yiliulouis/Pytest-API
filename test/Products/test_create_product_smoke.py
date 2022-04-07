
from src.Utilities.GenericUtilities import generate_random_string
from src.Helper.product_helper import ProductHelper
from src.DataAccessObject.Products_dao import ProductDAO
import pytest

pytestmark = [pytest.mark.products, pytest.mark.smoke]

@pytest.mark.TCID26
def test_create_1_simple_product():

    #generate the data
    payload = dict()
    payload['name'] = generate_random_string(7)
    payload['type'] = 'simple'
    payload['regular_price'] = '10.99'


    #make the call
    product_rs = ProductHelper().call_create_product(payload)

    #verify the response is not empty
    assert product_rs, f"Create product api response is empty. Payload is {payload}"
    assert product_rs['name'] == payload['name'], f"create product api call has unexpected name"\
        f"expected:{payload['name']}, Actual:{product_rs['name']}"

    #verify the product in DB
    product_id = product_rs['id']
    db_product =ProductDAO().get_product_by_id(product_id)

    assert payload['name'] == db_product[0]['post_title'],f"create product title in DB doesn't match title in API."\
        f"DB:{db_product[0]['post_title']}. API:{payload['name']}"

