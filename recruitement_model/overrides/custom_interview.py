import frappe
from frappe import _
from hrms.hr.doctype.interview.interview import Interview as ERPInterview

class CustomInterview(ERPInterview):
    def validate(self):
        if not self.job_applicant or not self.interview_round:
            return

        # Safely get applicant name from Job Applicant doctype
        applicant_name = frappe.db.get_value(
            "Job Applicant", self.job_applicant, "applicant_name"
        ) or self.job_applicant  # fallback

        # Check for duplicate interview round for same applicant
        duplicate = frappe.db.exists("Interview", {
            "job_applicant": self.job_applicant,
            "interview_round": self.interview_round,
            "name": ["!=", self.name]
        })

        if duplicate:
            frappe.throw(_(
                f"Interview round '{self.interview_round}' is already scheduled for applicant '{applicant_name}'."
            ))

