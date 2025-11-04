try:
    import frappe
    import erpnext
    from override_outstanding_function_in_erpnext.customer import get_customer_outstanding
    erpnext.selling.doctype.customer.customer.get_customer_outstanding = get_customer_outstanding
except Exception as e:
    print(f"Error applying override: {e}")
__version__ = "1.0.1"