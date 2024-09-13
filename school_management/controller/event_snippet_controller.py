# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request

class DynamicEventSnippets(http.Controller):
   """This class is for the getting values for dynamic event snippets"""
   @http.route('/recent-events', type='json', auth='public')
   def event_snippet(self):
       print('hi')
       recent_events = request.env['school.event'].sudo().search_read([],limit=4,order='start_date desc')
       values = {
           'recent_events': recent_events,
       }
       print(recent_events)
       return values