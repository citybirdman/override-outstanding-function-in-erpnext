import frappe
from erpnext.selling.doctype.customer.customer import Customer
from frappe.utils import flt

# class CustomCustomer(Customer):
@frappe.whitelist()
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

	outstanding_based_on_dn = 0
	
	outstanding_based_on_dn = frappe.db.sql(
		f"""
		WITH
		unbilled_delivery_notes AS (
		    SELECT DISTINCT dn.name, dn.grand_total
		    FROM `tabDelivery Note` dn
		    INNER JOIN `tabDelivery Note Item` dni ON dn.name = dni.parent
		    WHERE dn.docstatus = 1 AND dni.docstatus = 1 AND dn.is_return = 0 AND dn.status NOT IN ('Closed', 'Completed')
		    AND dn.name NOT IN (
		        SELECT DISTINCT sii.delivery_note
		        FROM `tabSales Invoice Item` sii
		        INNER JOIN `tabSales Invoice` si ON sii.parent = si.name
		        WHERE si.docstatus = 1 AND sii.docstatus = 1 AND si.is_return = 0
		        AND si.is_debit_note = 0 AND update_stock = 0 AND sii.delivery_note IS NOT NULL AND sii.delivery_note != ''
		        AND si.customer = %s AND si.company = %s
		    )
		    AND dni.against_sales_order IN (
		        SELECT name
		        FROM `tabSales Order`
		        WHERE docstatus = 1 AND status = 'Closed'
		        AND customer = %s AND company = %s
		    )
		    AND dn.customer = %s AND dn.company = %s
		)
		SELECT SUM(grand_total)
		FROM unbilled_delivery_notes""",
		(customer, company),
		)
	
	outstanding_based_on_dn = flt(outstanding_based_on_dn[0][0]) if outstanding_based_on_dn else 0
	
	return outstanding_based_on_gle + outstanding_based_on_so + outstanding_based_on_dn
