# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class StudentRegistrationWebsiteController(http.Controller):
    """to pass and get data from webpage"""
    @http.route(['/students'], type="http", auth="public", website="True")
    def student_data(self, **post):
       """to pass records of all students to webpage"""
       student_registration_data = request.env['student.registration'].sudo().search([])
       values = {
           'records': student_registration_data
       }
       return request.render("school_management.student_data_website_template", values)

    @http.route(['/student-registration'], type="http", auth="public", website="True")
    def student_registration(self, **post):
        """goes to student creation menu"""
        return request.render("school_management.student_registration_website_template")

    @http.route(['/contactus-thank-you'], type="http", auth="public", website="True")
    def student_create(self, **post):
        """creates student and return to main menu"""
        request.env['student.registration'].sudo().create({
            'first_name': post.get('first_name'),
            'last_name': post.get('last_name'),
            'email': post.get('email'),
            'Phone': post.get('phone'),
            'communication_street': post.get('communication_street'),
            'communication_city': post.get('communication_city'),
            'same_as_communication': post.get('permanent_address_same_as_above'),
            'permanent_street': post.get('permanent_street'),
            'permanent_city': post.get('permanent_city'),
        })
        return request.redirect('/students')
