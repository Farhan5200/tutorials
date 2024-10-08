# -*- coding: utf-8 -*-


import html2text
from odoo import http
from odoo.http import request


class EventCreationWebsiteController(http.Controller):
    """to pass and get data from webpage event main menu"""
    @http.route(['/events'], type="http", auth="public", website="True")
    def event_data(self, **post):
       """to pass records of all events to webpage"""
       events_data = request.env['school.event'].sudo().search([])
       status = dict(request.env['school.event']._fields['status'].selection)
       values = {
           'records': events_data,
           'status': status,
       }
       return request.render("school_management.events_data_website_template", values)


    @http.route(['/event-creation'], type="http", auth="public", website="True")
    def event_creation(self, **post):
        """goes to event creation menu"""
        club_rec = request.env['school.club'].search([])
        values = {
            'club_rec': club_rec,
        }
        return request.render("school_management.event_creation_website_template", values)

    @http.route(['/event-creation-success'], type="http", auth="public", website="True")
    def event_creation_success(self, **post):
        """creates event and return to main menu"""
        club = []
        for i in post.get('club_id_storing'):
            if i == ',':
                pass
            else:
                club.append(int(i))
        request.env['school.event'].sudo().create({
            'name': post.get('name'),
            'start_date': post.get('start_date'),
            'end_date': post.get('end_date'),
            'club_ids': club,
            'description': post.get('description'),
        })
        return request.redirect("/events")


    @http.route(['/event/<int:id>'], type="http", auth="public", website="True")
    def event_details_page(self, id):
        """goes to selected event page"""
        description = ''
        selected_event = request.env['school.event'].browse(id)
        club_rec = request.env['school.club'].search([])
        if selected_event.description:
            description = html2text.html2text(selected_event.description)
        values = {
            'selected_event': selected_event,
            'club_rec': club_rec,
            'description': description,
        }
        return request.render("school_management.selected_event_website_template", values)

    @http.route(['/event/delete'], type='json',  auth="public")
    def event_delete(self, **kwargs):
        """deletes the selected event"""
        selected_event_id = int(kwargs.get('id'))
        selected_event = request.env['school.event'].sudo().browse(selected_event_id)
        selected_event.unlink()
        return True

    @http.route(['/event/update'], type="http", auth="public", website="True")
    def event_update(self, **post):
        """updates the selected event"""
        selected_event = request.env['school.event'].browse(int(post.get('selected_event_id')))
        club = []
        for rec in post.get('event_show_club_id_storing'):
            if rec == ',':
                pass
            else:
                club.append(int(rec))
        selected_event.update({
             'name': post.get('event_show_name'),
            'start_date': post.get('event_show_start_date'),
            'end_date': post.get('event_show_end_date'),
            'club_ids': club,
            'description': post.get('description'),
        })
        return request.redirect('/events')


