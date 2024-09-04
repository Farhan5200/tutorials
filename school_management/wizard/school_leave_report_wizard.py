# -*- coding: utf-8 -*-

from odoo import api, fields,models
from odoo.tools import date_utils


class SchoolLeaveReportWizard(models.TransientModel):
    _name = "school.leave.report.wizard"
    _description = "School Leave Report Wizard"

    interval = fields.Selection([
        ('this_month', 'This Month'),
        ('this_week', 'This Week'),
        ('this_day', 'This Day'),
        ('custom', 'Custom')
    ], string="Interval", default="custom", required=True)

    from_date = fields.Date(string="From")
    to_date = fields.Date(string="To")
    class_id = fields.Many2one('school.class', string="Class")
    student_id = fields.Many2one('student.registration', domain="[('current_class_id', '=', class_id)]", string="Student")


    def action_print_report(self):
        data={
            'select_student_name': self.student_id.first_name,
            'select_class_name': self.class_id.name,
            'interval': self.interval,
            'from_date': self.from_date,
            'to_date': self.to_date
        }

        return self.env.ref('school_management.action_report_school_leave').report_action(None, data=data)

class AllLeaveReport(models.AbstractModel):
    _name = "report.school_management.report_leave"
    _description = "All leave report"

    @api.model
    def _get_report_values(self, docids, data=None):
        select_student_name = data['select_student_name']
        select_class_name = data['select_class_name']
        interval = data['interval']
        from_date = data['from_date']
        to_date = data['to_date']
        today = fields.Date.today()
        report_type = {'report_type': 'Complete Report',
                       'interval': interval}

        query = """select student_registration.first_name as student_name, school_class.name as class_name, 
        school_leaves.start_date, school_leaves.end_date, school_leaves.reason, school_leaves.total_days as duration, 
        school_leaves.half_day, school_leaves.fn_or_an from((school_leaves inner join student_registration on 
        student_registration.id =  school_leaves.student_id) inner join school_class on school_class.id = 
        student_registration.current_class_id)"""

        if interval == 'this_month':
            from_date = date_utils.start_of(today, "month")
            to_date = date_utils.end_of(today, "month")
            report_type['report_type'] = 'This Month Report'

        if interval == 'this_week':
            from_date = date_utils.start_of(today, "week")
            to_date = date_utils.end_of(today, "week")
            report_type['report_type'] = 'This Week Report'

        if interval == 'this_day':
            from_date = today
            to_date = today
            report_type['report_type'] = 'Today Report'

        if select_class_name and interval and not select_student_name:
            query += """ where school_class.name = '%s'and school_leaves.start_date >=
             '%s'and school_leaves.start_date <= '%s'""" % (select_class_name, from_date, to_date)
        if interval and not select_class_name and not select_student_name:
            query += " where school_leaves.start_date >= '%s' and school_leaves.start_date <= '%s'" % (from_date, to_date)
        if select_class_name and not interval and not select_student_name:
            query += " where school_class.name = '%s'" %select_class_name
        if select_class_name and select_student_name and interval:
            query += (""" where school_class.name = '%s' and student_registration.first_name = '%s' and 
            school_leaves.start_date >= '%s'and school_leaves.start_date <= '%s'"""
                      %(select_class_name, select_student_name, from_date, to_date))
        if select_class_name and select_student_name and not interval:
            query += (""" where school_class.name = '%s' and student_registration.first_name = '%s'"""
                      %(select_class_name, select_student_name))
        if not select_class_name and select_student_name and interval:
            query += """ where student_registration.first_name = '%s' and school_leaves.start_date >= '%s' 
            and school_leaves.start_date <= '%s'""" %(select_student_name, from_date, to_date)
        if not select_class_name and select_student_name and not interval:
            query += """ where student_registration.first_name = '%s'""" %select_student_name



        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        return {
            'docs': report,
            'report_type': report_type
        }

