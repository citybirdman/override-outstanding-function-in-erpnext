_version__ = "1.0.1"
import erpnext
#import override_outstanding_function_in_erpnext
from override_outstanding_function_in_erpnext.customer import get_customer_outstanding
erpnext.selling.doctype.customer.customer.get_customer_outstanding = get_customer_outstanding
