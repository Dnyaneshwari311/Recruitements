import frappe

def get_context(context):
    jobs = frappe.db.sql("""
        SELECT name, job_title, status, route, company, posted_on
        FROM `tabJob Opening`
        WHERE publish = 1
        ORDER BY
            CASE WHEN status = 'Open' THEN 0 ELSE 1 END,
            posted_on DESC
    """, as_dict=True)

    context.jobs = jobs
    context.title = "Job Openings"
    context.no_cache = True
    context.parents = [{"route": "/", "title": "Home"}]
    return context
