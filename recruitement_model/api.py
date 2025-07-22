import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def accept_offer(job_offer):
    if not job_offer:
        return "Missing job_offer parameter"

    doc = frappe.get_doc("Job Offer", job_offer)
    doc.status = "Accepted"
    doc.save(ignore_permissions=True)
    frappe.db.commit()

    return frappe.respond_as_web_page(
        title="Offer Accepted",
        html="""
        <div style="text-align:center; padding:60px; font-family:sans-serif;">
            <h1 style="color:green;">🎉 Thank you for accepting the job offer!</h1>
            <p>We look forward to having you onboard.</p>
        </div>
        """,
        success=True,
        indicator_color="green"
    )

@frappe.whitelist(allow_guest=True)
def reject_offer(job_offer):
    if not job_offer:
        return "Missing job_offer parameter"

    doc = frappe.get_doc("Job Offer", job_offer)
    doc.status = "Rejected"
    doc.save(ignore_permissions=True)
    frappe.db.commit()

    return frappe.respond_as_web_page(
        title="Offer Rejected",
        html="""
        <div style="text-align:center; padding:60px; font-family:sans-serif; background:#fff4f4;">
            <h1 style="color:red;">❌ You have rejected the job offer</h1>
            <p>Thank you for your response. Wishing you the best!</p>
        </div>
        """,
        success=True,
        indicator_color="red"
    )
