import pytest
from src.DataAccessObject.Customers_dao import CustomersDao
from src.Utilities.RequestsUtility import RequestsUtility
from src.DataAccessObject.Products_dao import ProductDAO
from src.Helper.product_helper import ProductHelper

pytestmark = [pytest.mark.products, pytest.mark.smoke]

@pytest.mark.TCID24
def test_list_all_products():
    #get all products from the DB
    prod_dao = CustomersDao()
    existing_product = prod_dao.get_all_product_from_db()

    #make the call
    req_helper = RequestsUtility()
    api_all_product_info = req_helper.get(endpoint = 'products')

    #products are not empty i
    assert api_all_product_info, f"Products are empty in api"




@pytest.mark.TCID25
def test_get_product_by_id():
    
    #get the product from DB
    rand_products = ProductDAO().get_random_product_from_db(1)
    rand_produc_id = rand_products[0]['ID']
    db_product_name = rand_products[0]['post_title']

    #make the call
    product_helper = ProductHelper()
    rs_api = product_helper.get_product_by_id(rand_produc_id)
    api_name = rs_api['name']


    
    #verify the response
    assert db_product_name == api_name, f"get product by ID returned wrong product. Id: {rand_produc_id}"\
        f"DB Name: {db_product_name}. API Name: {api_name} "
