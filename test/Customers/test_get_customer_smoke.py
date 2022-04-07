
import logging as logger
import pytest
from src.Utilities.RequestsUtility import RequestsUtility


@pytest.mark.TCID30
@pytest.mark.customer
def test_get_all_customers():
    req_helper = RequestsUtility()
    rs_api = req_helper.get('customers')
    logger.debug(f"Response of list all:{rs_api}")

    #import pdb; pdb.set_trace()