from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice

class CustomSalesInvoice(SalesInvoice):
    def check_sales_order_on_hold_or_close(self, ref_fieldname):
        pass