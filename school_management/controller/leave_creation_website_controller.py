# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class LeaveCreationWebsiteController(http.Controller):
    """to pass and get data from webpage leave main menu"""
    @http.route(['/leaves'], type="http", auth="public", website="True")
    def leave_data(self, **post):
       """to pass records of all events to webpage"""
       leave_data = request.env['school.leaves'].sudo().search([])
       values = {
           'records': leave_data
       }
       return request.render("school_management.leaves_data_website_template", values)

    @http.route(['/leave/<int:id>'], type="http", auth="public", website="True")
    def leave_details_page(self, id):
        selected_leave = request.env['school.leaves'].browse(id)
        fn_or_an = dict(request.env['school.leaves']._fields['fn_or_an'].selection)
        values = {
            'selected_leave': selected_leave,
            'fn_or_an': fn_or_an,
        }
        return request.render("school_management.selected_leave_website_template", values)

    @http.route(['/leave-creation'], type="http", auth="public", website="True")
    def leave_creation_page(self):
        student_rec = request.env['student.registration'].search([('status', '=', 'registration')])
        values = {
            'student_rec': student_rec,
        }
        return request.render("school_management.leave_creation_website_template", values)

    @http.route(['/leave-creation-success'], type="http", auth="public", website="True")
    def leave_creation_success_page(self, **post):
        if post.get('leave_half_day'):
            request.env['school.leaves'].create({
                'student_id': post.get('many2one_student'),
                'start_date': post.get('leave_start_date'),
                'half_day': True,
                'fn_or_an': post.get('leave_an_or_fn'),
                'reason': post.get('leave_reason')
            })
        else:
            request.env['school.leaves'].create({
                'student_id': post.get('many2one_student'),
                'start_date': post.get('leave_start_date'),
                'end_date': post.get('leave_end_date'),
                'half_day': False,
                'reason': post.get('leave_reason')
            })
        return request.redirect("/leaves")

    @http.route(['/leave/class'], type='json',  auth="public")
    def leave_class(self, **kwargs):
        student_id = int(kwargs.get('id'))
        selected_class = request.env['student.registration'].browse(student_id).current_class_id.name
        return selected_class



