import frappe
from frappe import _

@frappe.whitelist()
def send_shortlist_email(docname):
    doc = frappe.get_doc("Job Applicant", docname)

    if not doc.email_id:
        frappe.throw(_("No email address found for the applicant."))

    message = f"""
    <p>Dear {doc.applicant_name},</p>

    <p>Congratulations! You have been <strong>shortlisted</strong> for the position of <strong>{doc.job_title}</strong> at Excellent Minds Software Technologies.</p>

    <p>Our team will reach out to you shortly with the interview schedule.</p>

    <p>Best regards,<br>
    HR Department<br>
    Excellent Minds Software Technologies Pvt. Ltd.</p>
    """

    try:
        frappe.sendmail(
            recipients=[doc.email_id],
            subject="Shortlisted for Interview – Excellent Minds",
            message=message,
            reference_doctype=doc.doctype,
            reference_name=doc.name,
        )
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Shortlisting Email Failed")
        frappe.throw(_("Failed to send the email. Please check email configuration."))

    frappe.msgprint(_("Shortlist email sent successfully."))
