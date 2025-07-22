import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import get_url_to_form, format_datetime


class Interview(Document):
    pass


@frappe.whitelist()
def reschedule_interview(docname, scheduled_on, from_time, to_time):
    doc = frappe.get_doc("Interview", docname)

    if scheduled_on == doc.scheduled_on and from_time == doc.from_time and to_time == doc.to_time:
        frappe.msgprint(
            _("No changes found in timings."), indicator="orange", title=_("Interview Not Rescheduled")
        )
        return

    original_date = doc.scheduled_on
    original_from_time = doc.from_time
    original_to_time = doc.to_time

    doc.db_set({
        "scheduled_on": scheduled_on,
        "from_time": from_time,
        "to_time": to_time
    })

    doc.notify_update()

    # ✅ Collect actual recipients
    recipients = []

    if doc.get("custom_applicant_email"):
        recipients.append(doc.custom_applicant_email)

    # ✅ Fetch from interview_details child table
    if doc.get("interview_details"):
        for row in doc.interview_details:
            if row.interviewer:
                interviewer_email = frappe.db.get_value("User", row.interviewer, "email")
                if interviewer_email and interviewer_email not in recipients:
                    recipients.append(interviewer_email)

    # ✅ Format times
    try:
        from_time_str = doc.from_time.strftime("%H:%M")
        to_time_str = doc.to_time.strftime("%H:%M")
    except Exception:
        from_time_str = str(doc.from_time)[:5]
        to_time_str = str(doc.to_time)[:5]

    # ✅ Email body with dynamic info
    interview_url = get_url_to_form(doc.doctype, doc.name)

    message = f"""
    <p>Dear {doc.get('custom___applicant_name', 'Candidate')},</p>

    <p>We are pleased to inform you that your interview with Excellent Minds has been <strong>Rescheduled</strong>. Below are the details of your interview:</p>

    <p><strong>Company Name:</strong> Excellent Minds Software Technologies India Pvt. Ltd.</p>

    <p><strong>Scheduled On:</strong> {format_datetime(doc.scheduled_on)}</p>

    <p><strong>Scheduled Time:</strong> {from_time_str} - {to_time_str}</p>

    <p><strong>Interview Type:</strong> Online</p>

    <p><strong>Google Meet Link:</strong>
        <a href="{'https://meet.google.com/usn-tmxn-uzq'}">
            {'https://meet.google.com/usn-tmxn-uzq'}
        </a>
    </p>

    <p>Please ensure that you are available at the specified time and prepared for the interview. If you have any questions or need to reschedule, please contact us at <a href="mailto:careers@excellminds.com">careers@excellminds.com</a> as soon as possible.</p>

    <p>Please confirm your availability.</p>

    <hr />
    <p style="font-weight: bold;">Best regards,</p>
    <div>Project Manager</div>
    <div style="color: green;">Excellent Minds Software Technologies India Pvt. Ltd.</div>
    <div style="font-weight: bold;">Website - <a href="http://www.excellminds.com" style="color: blue;">www.excellminds.com</a></div>
    <br/>
    <p><a href="{interview_url}">Click here to view the updated interview</a></p>
    """

    try:
        frappe.sendmail(
            recipients=recipients,
            subject=_("Your Interview Has Been Rescheduled"),
            message=message,
            reference_doctype=doc.doctype,
            reference_name=doc.name,
        )
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Interview Reschedule Email Failed")
        frappe.msgprint(_("Failed to send the Interview Reschedule notification."))

    frappe.msgprint(_("Interview Rescheduled successfully"), indicator="green")
