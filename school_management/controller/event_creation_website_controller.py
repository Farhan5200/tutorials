# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class EventCreationWebsiteController(http.Controller):
    """to pass and get data from webpage event main menu"""
    @http.route(['/events'], type="http", auth="public", website="True")
    def event_data(self, **post):
       """to pass records of all events to webpage"""
       events_data = request.env['school.event'].sudo().search([])
       values = {
           'records': events_data
       }
       return request.render("school_management.events_data_website_template", values)


    @http.route(['/event-creation'], type="http", auth="public", website="True")
    def event_creation(self, **post):
        """goes to event creation menu"""
        return request.render("school_management.event_creation_website_template")

    @http.route(['/event-creation-success'], type="http", auth="public", website="True")
    def event_creation_success(self, **post):
        """creates event and return to main menu"""
        request.env['school.event'].sudo().create({
            'name': post.get('name'),
            'start_date': post.get('start_date'),
            'end_date': post.get('end_date'),
            'club_ids': post.get('club'),
        })
        return request.redirect("/events")