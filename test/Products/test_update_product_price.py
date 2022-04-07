import pytest
from src.DataAccessObject.Products_dao import ProductDAO
from src.Helper.product_helper import ProductHelper
from src.Utilities import GenericUtilities
import random

pytestmark = [pytest.mark.products, pytest.mark.regression]
@pytest.mark.TCID61
def test_update_product_price():
    #Note: updated "regular_price" should be automatically update "price" field

    #create help object and get random product from DB
    product_dao=ProductDAO()
    product_helper = ProductHelper()


    #create a new product or using an existing product
    # for this test the 'sale_price' of the product must be empty. If product has sale price, updating the 'regular_price'
    # does not update the 'price'. So get a bunch of products and loop until you find one that is not on sale. 

    rand_products = product_dao.get_random_product_from_db(30)
    for product in rand_products:
        product_id = product['ID']
        product_data = product_helper.call_retrieve_products(product_id)
        if product_data['on_sale']:
            continue # the product is on sale
        else:
            break #the product don't have on_sale price
    else: #If all inthe list are on sale then take random one and update the sale price
        test_product = random.choice(rand_products)
        product_id = test_product['ID']
        product_helper.call_update_products(product_id,{'sale_price':''})

    

    #make the update product call
    new_price =str(random.randint(10,100))+'.'+str(random.randint(10,99))
    payload = dict()
    payload['regular_price'] = new_price

    rs_update = product_helper.call_update_products(product_id,payload)

    #import pdb;pdb.set_trace()
    #verify in the response or call to retrieve product

    assert rs_update['price'] == new_price, f"Update product call API response. Update the 'regular_price' did not"\
        "Update the 'Price' field. Price field actual value: {rs_update['price']}, but expected: {new_price}"

    assert rs_update['regular_price'] == new_price, f"Update product call API response. Update the 'regular_price' did not"\
        "Update the 'Price' field. Price field actual value: {rs_update['regular_price']}, but expected: {new_price}"

    # get the product after the update and verify response
    rs_product = product_helper.call_update_products(product_id)
    assert rs_product['price'] == new_price, f"Update product call API response. Update the 'regular_price' did not"\
        "Update the 'Price' field. Price field actual value: {rs_update['price']}, but expected: {new_price}"
    assert rs_product['regular_price'] == new_price, f"Update product call API response. Update the 'regular_price' did not"\
        "Update the 'Price' field. Price field actual value: {rs_update['regular_price']}, but expected: {new_price}"



@pytest.mark.TCID63test
def test_update_sale_price_update_on_sale_Louis_version():
    #get product from db, select product whose sales price is 0
    product_dao = ProductDAO()
    product_helper = ProductHelper()

    products = product_dao.get_random_product_from_db(30)
    for product in products:
        product_id = product['ID']
        product_data = product_helper.call_retrieve_products(product_id)
        if product_data['sale_price']=='':
            continue
        else:
            break
    else:
        test_product = product['ID']
        test_product_id = product['ID']
        product_sale_price = product['sale_price']


    #Update sales_price, make the call
    sale_price = str(random.randint(10,99))+'.'+str(random.randint(10,99))
    payload = dict()
    payload['sale_price'] = sale_price
    rs_product = product_helper.call_update_products(product_id,payload)
    import pdb; pdb.set_trace()


    #verify sale price is updated, verify on_sale field is updated
    assert sale_price == rs_product['sale_price'], f"API sales price is not update"
    assert rs_product['on_sale'] == True, f"on_sale field is not updated. Actual: {rs_product['on_sale']}, expected: True"


@pytest.mark.TCID63
@pytest.mark.TCID64
def test_update_sale_price_update_on_sale():
    #create a product and pass the payload
    product_helper = ProductHelper()

    regular_price = str(random.randint(10,100))+'.'+str(random.randint(10,99))
    payload=dict()
    payload['name'] = GenericUtilities.generate_random_string(5)
    payload['type'] = 'simple'
    payload['regular_price'] = regular_price
    product_info = product_helper.call_create_product(payload)
    product_id = product_info['id']

    assert not product_info['on_sale'], f"on_sale field is not empty"
    assert not product_info['sale_price'], f"sale_price is not empty"


    #Make the call, verify the update on_sale field is update
    #TCID63
    sale_price = float(regular_price) * 0.75
    payload['sale_price'] = str(sale_price)
    product_update = product_helper.call_update_products(product_id,payload)
    product_update_sale_price = product_update['sale_price']
    product_after_update = product_helper.call_retrieve_products(product_id)
    product_after_sale_price = product_after_update['sale_price']
    assert product_update_sale_price==product_after_sale_price, f"sale_price is not updated after the API call. Exptected: {product_update_sale_price}"\
        "Actual: {product_after_sale_price}"
    assert product_after_update['on_sale'] == True, f"on_sale field is not updated after the API Call"


    #Make the call, verify when sale_price ='', on_sale is false
    #TCID64
    payload['sale_price'] = ''
    product_update = product_helper.call_update_products(product_id,payload)
    product_update_sale_price = product_update['sale_price']
    product_update_on_sale = product_update['on_sale']
    assert not product_update_sale_price, f"sale_price should be zero, actual:{product_update_sale_price}"
    assert not product_update_on_sale, f"on_sale should be False, actual:{product_update_on_sale}"

    
@pytest.mark.TCID65
def test_sale_price_update():
    #get product info from DB, make sure the product is not on sale
    product_helper=ProductHelper()
    product_dao = ProductDAO()
    rand_product = product_dao.get_random_product_not_on_sale_from_db(1)
    product_id = rand_product[0]['ID']
    product_info = product_helper.call_retrieve_products(product_id)
    regular_price = product_info['regular_price']

    assert not product_info['on_sale'], f"this product is on sale"

    #create payload and update the sale price
    sale_price = float(regular_price) *0.75
    payload= dict()
    payload['sale_price'] = str(sale_price)
    rs_sale_price_update = product_helper.call_update_products(product_id,payload)
    updated_sale_price = rs_sale_price_update['sale_price']

    #verify sale price is updated
    assert float(updated_sale_price) == sale_price, f"sale price is not updated. Actual:{float(updated_sale_price)}, expected:{sale_price}"

