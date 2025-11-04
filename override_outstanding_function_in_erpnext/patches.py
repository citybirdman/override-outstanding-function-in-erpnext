import frappe

def apply_patch(bootinfo=None):
    try:
        import erpnext.selling.doctype.customer.customer as customer
        from override_outstanding_function_in_erpnext.customer import get_customer_outstanding
        customer.get_customer_outstanding = get_customer_outstanding
    except Exception:
        frappe.log_error(message=frappe.get_traceback(), title="patches.apply_patch")