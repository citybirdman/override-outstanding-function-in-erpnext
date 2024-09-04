import frappe
from erpnext.selling.doctype.customer.customer import Customer
from frappe.utils import flt

# class CustomCustomer(Customer):
def get_customer_outstanding(customer, company, ignore_outstanding_sales_order=False, cost_center=None):
    # Outstanding based on GL Entries
	cond = ""
	if cost_center:
	    lft, rgt = frappe.get_cached_value("Cost Center", cost_center, ["lft", "rgt"])
	
	    cond = f""" and cost_center in (select name from `tabCost Center` where
		lft >= {lft} and rgt <= {rgt})"""
	
	outstanding_based_on_gle = frappe.db.sql(
	    f"""
	    select sum(debit) - sum(credit)
	    from `tabGL Entry` where party_type = 'Customer'
	    and is_cancelled = 0 and party = %s
	    and company=%s {cond}""",
	    (customer, company),
	)
	
	outstanding_based_on_gle = flt(outstanding_based_on_gle[0][0]) if outstanding_based_on_gle else 0
	
	# Outstanding based on Sales Order
	outstanding_based_on_so = 0

# if credit limit check is bypassed at sales order level,
# we should not consider outstanding Sales Orders, when customer credit balance report is run
if not ignore_outstanding_sales_order:
    outstanding_based_on_so = frappe.db.sql(
	"""
	select sum(base_grand_total*(100 - per_billed)/100)
	from `tabSales Order`
	where customer=%s and docstatus = 1 and company=%s
	and per_billed < 100 and status != 'Closed'""",
	(customer, company),
    )

    outstanding_based_on_so = flt(outstanding_based_on_so[0][0]) if outstanding_based_on_so else 0
return outstanding_based_on_gle + outstanding_based_on_so
