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
        country = request.env['res.country'].search([])
        values = {
            'country_id': country,
        }
        return request.render("school_management.student_registration_website_template", values)


    @http.route(['/student-registration-success'], type="http", auth="public", website="True")
    def student_create(self, **post):
        """creates student and return to main menu"""
        print(post)
        request.env['student.registration'].sudo().create({
            'first_name': post.get('first_name'),
            'last_name': post.get('last_name'),
            'email': post.get('email'),
            'Phone': post.get('phone'),
            'communication_street': post.get('communication_street'),
            'communication_city': post.get('communication_city'),
            'communication_country_id': post.get('communication_country'),
            'same_as_communication': post.get('permanent_address_same_as_above'),
            'permanent_street': post.get('permanent_street'),
            'permanent_city': post.get('permanent_city'),
            'permanent_country_id': post.get('permanent_country'),
            'date_of_birth': post.get('date_of_birth'),
            'gender': post.get('gender'),
        })
        return request.redirect('/students-form-success')

    @http.route(['/student/<int:id>'], type="http", auth="public", website="True")
    def selected_student_details(self, id):
        """show selected student details"""
        selected_student = request.env['student.registration'].browse(id)
        values = {
            'selected_student': selected_student,
        }
        return request.render('school_management.selected_student_website_template', values)

