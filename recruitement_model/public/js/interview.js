frappe.ui.form.on('Interview', {
    onload: function(frm) {
        if (frm.doc.job_opening && frm.is_new()) {
            populate_interview_skills(frm);
        }
    },

    refresh: function (frm) {
        if (frm.doc.docstatus === 2 || frm.doc.__islocal) return;

        if (frm.doc.status === "Pending") {
            frm.add_custom_button(
                __("Reschedule Interview"),
                function () {
                    frm.events.show_reschedule_dialog(frm);
                },
                __("Actions")
            );
        }
    },

    job_opening: function(frm) {
        if (!frm.doc.job_opening) return;
        populate_interview_skills(frm);
    },

    show_reschedule_dialog: function (frm) {
        frappe.prompt([
            {
                fieldname: 'scheduled_on',
                label: 'New Date',
                fieldtype: 'Date',
                reqd: 1
            },
            {
                fieldname: 'from_time',
                label: 'New From Time',
                fieldtype: 'Time',
                reqd: 1
            },
            {
                fieldname: 'to_time',
                label: 'New To Time',
                fieldtype: 'Time',
                reqd: 1
            }
        ],
        function (values) {
            frm.call({
                method: "recruitement_model.doctype.interview.interview.reschedule_interview",
                args: {
                    docname: frm.doc.name,
                    scheduled_on: values.scheduled_on,
                    from_time: values.from_time,
                    to_time: values.to_time
                },
                freeze: true,
                callback: function (r) {
                    if (!r.exc) {
                        frappe.show_alert({
                            message: __("Interview rescheduled"),
                            indicator: "green"
                        });
                        frm.reload_doc();
                    }
                }
            });
        },
        __("Reschedule Interview"),
        __("Reschedule"));
    }
});

function populate_interview_skills(frm) {
    console.log("Fetching skills for job opening:", frm.doc.job_opening);

    frappe.call({
        method: "frappe.client.get",
        args: {
            doctype: "Job Opening",
            name: frm.doc.job_opening
        },
        callback: function(response) {
            const job = response.message;
            console.log("Job Opening Response:", job);

            if (job && job.custom_skills && job.custom_skills.length > 0) {
                frm.clear_table("custom_interview_skills__table");
                job.custom_skills.forEach(skill_row => {
                    let new_row = frm.add_child("custom_interview_skills__table");
                    new_row.skill = skill_row.skill;
                    new_row.skill_type = skill_row.skill_type;
                });
                frm.refresh_field("custom_interview_skills__table");
                console.log("Interview skills populated.");
            } else {
                frappe.msgprint("No skills found in the selected Job Opening.");
            }
        }
    });
}
