from hashlib import new
import frappe
import json
from frappe.model.mapper import make_mapped_doc


@frappe.whitelist()
def sales_order_api(reference_doc_id):
    sal_ord=make_mapped_doc(method="erpnext.selling.doctype.quotation.quotation.make_sales_order",source_name=reference_doc_id)
    sal_frappe_json=frappe.as_json(sal_ord)
    sal_ord_json=json.loads(sal_frappe_json)
    sal_ord_json.pop('docstatus',None)
    sal_ord_json['doctype']="Sales Order"
    sal_ord_json['order_type']="Shopping Cart"
    new_order=frappe.get_doc(sal_ord_json)
    new_order.save(ignore_permissions=True)
    new_order.submit()

    return new_order

