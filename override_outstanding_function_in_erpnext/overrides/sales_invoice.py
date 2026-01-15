from stock_delivered_unbilled.stock_delivered_unbilled.overrides.sales_invoice import CustomSalesInvoice as SalesInvoice
# import frappe
# from frappe.model.base_document import get_controller
# class_controller = get_controller("Sales Invoice")
# frappe.get
class CustomSalesInvoice(SalesInvoice):
    def check_sales_order_on_hold_or_close(self, ref_fieldname):
        pass