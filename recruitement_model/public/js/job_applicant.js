frappe.ui.form.on("Job Applicant", {
    onload: function (frm) {
        // ✅ Fetch interview rounds from Job Opening
        if (frm.doc.job_title) {
            let job_opening_id = frm.doc.job_title;

            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Job Opening",
                    name: job_opening_id
                },
                callback: function (r) {
                    if (r.message) {
                        frm.custom_interview_rounds = r.message.custom_interview_rounds || [];
                    }
                }
            });
        }

        // ✅ Override create_dialog to show round dropdown
        frm.events.create_dialog = function (frm) {
            if (!frm.custom_interview_rounds || frm.custom_interview_rounds.length === 0) {
                frappe.msgprint("No Interview Rounds found for selected Job Opening.");
                return;
            }

            // Get only round names
            let round_options = frm.custom_interview_rounds.map(r => r.round_name);

            let d = new frappe.ui.Dialog({
                title: "Enter Interview Round",
                fields: [
                    {
                        label: "Interview Round",
                        fieldname: "interview_round",
                        fieldtype: "Select",
                        options: round_options,
                        reqd: 1
                    }
                ],
                primary_action_label: __("Create Interview"),
                primary_action(values) {
                    frm.events.create_interview(frm, values);
                    d.hide();
                }
            });

            d.show();
        };

        // ✅ Use ERPNext’s standard create_interview logic
        frm.events.create_interview = function (frm, values) {
            frappe.call({
                method: "hrms.hr.doctype.job_applicant.job_applicant.create_interview",
                args: {
                    doc: frm.doc,
                    interview_round: values.interview_round,
                },
                callback: function (r) {
                    if (r.message) {
                        var doclist = frappe.model.sync(r.message);
                        frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
                    }
                }
            });
        };
    }, // ⬅️⏹️ END OF onload FUNCTION — insert refresh below this line

    // ✅ INSERTED HERE: Add shortlist button on form
    refresh: function (frm) {
        if (!frm.doc.__islocal) {
            frm.add_custom_button("Shortlist Applicant", () => {
                frappe.call({
                    method: "recruitement_model.doctype.job_applicant.job_applicant.send_shortlist_email",
                    args: {
                        docname: frm.doc.name
                    },
                    freeze: true,
                    callback: function () {
                        frappe.msgprint("Shortlist email sent to applicant.");
                    }
                });
            }, __("Actions"));
        }
    }
});






