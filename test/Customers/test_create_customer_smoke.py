
import pytest 
import logging as logger
from src.Utilities.GenericUtilities import generate_random_email_and_password
from src.Helper.customer_helper import CustomerHelper
from src.DataAccessObject.Customers_dao import CustomersDao
from src.Utilities.RequestsUtility import RequestsUtility

@pytest.mark.TCID29
@pytest.mark.customer
def test_create_customer_only_email_password():



    logger.info("Test: create new cusomter with email and password only")
    
    rand_info = generate_random_email_and_password()

    logger.info(rand_info)
    email = rand_info['email']
    password = rand_info['password']
    import pdb; pdb.set_trace()


    # create payload 

    # make the call  - also reuseable
    cust_obj = CustomerHelper()
    cust_api_info = cust_obj.create_customer(email = email, password = password)
    #import pdb; pdb.set_trace()
    # verify email and first name in the response
    
    assert cust_api_info['email'] == email, f"Create Customer api return wrong email. Email:{email}"
    assert cust_api_info['first_name'] == '', f"Create Customer api return wrong first_name. But it should be empty"
    
    
    
    # verify status code of the call



    # verify customer is created in database - also reuseable
    cust_dao = CustomersDao()
    cust_info = cust_dao.get_customer_by_email(email)
    
    id_in_api = cust_api_info['id']
    id_in_db = cust_info[0]['ID']
    assert id_in_api==id_in_db, f'Create Customer response id not same as "ID" in database'\
        f'Email: {email}'
    
    
    #import pdb; pdb.set_trace()


@pytest.mark.TCID47
@pytest.mark.customer
def test_create_customer_fail_for_existing_email():

    #get the email from the database
    cust_dao = CustomersDao()
    existing_customer = cust_dao.get_random_customer_from_db()
    existing_email = existing_customer[0]['user_email']


    #call the api
    req_helper = RequestsUtility()

    payload = {"email":existing_email, "sassword":"Password1"}
    cust_api_info = req_helper.post(endpoint= 'customers',payload=payload, expected_status_code=400)

    assert cust_api_info['code'] == 'registration-error-email-exists', f"Create customer with existing user" \
        f"error 'code' is not correct. Expected: 'registration-error-email-exists', Actual:{cust_api_info['code']}"
    
