_version__ = "1.0.1"
from erpnext.selling.doctype.customer.customer import get_customer_outstanding as d
from override_outstanding_function_in_erpnext.customer import get_customer_outstanding
d = get_customer_outstanding
