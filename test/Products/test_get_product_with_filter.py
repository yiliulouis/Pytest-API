
import pytest
from datetime import datetime, timedelta
from src.Helper.product_helper import ProductHelper
from src.DataAccessObject.Products_dao import ProductDAO
import pdb





@pytest.mark.regression
class TestListProductsWithFilter(object):

    @pytest.mark.TCID51
    def test_list_products_with_filter_after(self):

        # create payload
        x_days_from_today = 300
        #_after_created_date = datetime.now().replace(microsecond=0) - timedelta(days = x_days_from_today)
        #after_created_date = _after_created_date.isoformat()

        tmp_date = datetime.now() - timedelta(days = x_days_from_today)
        after_created_date = tmp_date.strftime('%Y-%m-%dT%H:%M:%S')
        #%M - Minute as a zero-padded decimal number., %mMonth as a zero-padded decimal number.

        # make the call
        payload = dict()
        payload['after'] = after_created_date
        payload['per_page'] = 100
        rs_api = ProductHelper().call_list_products(payload)
        assert rs_api, f"Empty response for 'List products with filter"
        
        # get data from db
        db_product = ProductDAO().get_product_created_after_given_date(after_created_date)

        # verify response
        assert len(rs_api) == len(db_product), f"List products with filter 'after' returned unexpected number of products"\
            f"Expected: {len(db_product)}, Actual:{len(rs_api)} "

        ids_in_api = [i['id'] for i in rs_api]
        ids_in_db = [i['ID'] for i in db_product]

        ids_diff = list(set(ids_in_api) - set(ids_in_db))
        assert not ids_diff , f"List product with filer. Products Ids in response mismatch in db."
