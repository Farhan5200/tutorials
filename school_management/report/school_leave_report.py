# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import date_utils


class SchoolLeaveReport(models.AbstractModel):
    """For passing values to the leave report"""

    _name = "report.school_management.report_leave"
    _description = "All leave report"

    @api.model
    def _get_report_values(self, docids, data=None):
        """For passing values to the leave report"""

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
            if interval != 'custom':
                query += """ where school_class.name = '%s'and school_leaves.start_date >=
                 '%s'and school_leaves.start_date <= '%s'""" % (select_class_name, from_date, to_date)
            elif from_date and not to_date:
                query += " where school_class.name = '%s' and school_leaves.start_date >='%s'" %(select_class_name,from_date)
            elif to_date and not from_date:
                query += " where school_class.name = '%s' and school_leaves.start_date <= '%s'" %(select_class_name,to_date)
            elif from_date and to_date:
                query += """ where school_class.name = '%s' and school_leaves.start_date >= '%s' and 
                                school_leaves.start_date <= '%s'""" % (select_class_name, from_date, to_date)
            elif not from_date and not to_date:
                query += " where school_class.name = '%s'" %select_class_name


        if interval and not select_class_name and not select_student_name:
            if interval != 'custom':
                query += " where school_leaves.start_date >= '%s' and school_leaves.start_date <= '%s'" % (from_date, to_date)
            elif from_date and not to_date:
                query += " where school_leaves.start_date >='%s'" %from_date
            elif to_date and not from_date:
                query += " where school_leaves.start_date <= '%s'" %to_date
            elif from_date and to_date:
                query += " where school_leaves.start_date >= '%s' and school_leaves.start_date <= '%s'" % (
                    from_date, to_date)

        if select_class_name and not interval and not select_student_name:
            query += " where school_class.name = '%s'" %select_class_name

        if select_class_name and select_student_name and interval:
            if interval != 'custom':
                query += (""" where school_class.name = '%s' and student_registration.first_name = '%s' and 
                school_leaves.start_date >= '%s' and school_leaves.start_date <= '%s'"""
                          %(select_class_name, select_student_name, from_date, to_date))
            elif from_date and not to_date:
                query += """where school_class.name = '%s' and student_registration.first_name = '%s' and 
                school_leaves.start_date >= '%s'"""%(select_class_name, select_student_name, from_date)
            elif to_date and not from_date:
                query += """where school_class.name = '%s' and student_registration.first_name = '%s' and 
                school_leaves.start_date <= '%s'""" %(select_class_name, select_student_name, to_date)
            elif from_date and to_date:
                query += (""" where school_class.name = '%s' and student_registration.first_name = '%s' and 
                                school_leaves.start_date >= '%s' and school_leaves.start_date <= '%s'"""
                          % (select_class_name, select_student_name, from_date, to_date))
            elif not from_date and not to_date:
                query += ("""where school_class.name = '%s' and student_registration.first_name = '%s'"""
                          %(select_class_name, select_student_name))


        if select_class_name and select_student_name and not interval:
            query += (""" where school_class.name = '%s' and student_registration.first_name = '%s'"""
                      %(select_class_name, select_student_name))

        if not select_class_name and select_student_name and interval:
            if interval != "custom":
                query += """ where student_registration.first_name = '%s' and school_leaves.start_date >= '%s' 
                and school_leaves.start_date <= '%s'""" %(select_student_name, from_date, to_date)
            elif from_date and not to_date:
                query += (""" where student_registration.first_name = '%s' and school_leaves.start_date >= '%s'"""
                          % (select_student_name, from_date))
            elif to_date and not from_date:
                query += (""" where student_registration.first_name = '%s' and school_leaves.start_date <= '%s'"""
                          % (select_student_name, to_date))
            elif from_date and to_date:
                query += """ where student_registration.first_name = '%s' and school_leaves.start_date >= '%s' 
                                and school_leaves.start_date <= '%s'""" % (select_student_name, from_date, to_date)
            elif not from_date and not to_date:
                query += """ where student_registration.first_name = '%s'""" % select_student_name



        if not select_class_name and select_student_name and not interval:
            query += """ where student_registration.first_name = '%s'""" %select_student_name

        dates = {
            'from_date': from_date,
            'to_date': to_date,
            'current_date': today
        }



        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()

        if report:
            return {
                'docs': report,
                'report_type': report_type,
                'dates': dates
            }
        else:
            raise ValidationError('There are no records matching your condition')

