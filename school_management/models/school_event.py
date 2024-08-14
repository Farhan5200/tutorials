# -*- coding: utf-8 -*-

from odoo import fields, models


class SchoolEvent(models.Model):
    """to create event creation form"""
    _name = "school.event"
    _description = "School Event"

    name = fields.Char("Name", required=True)
    start_date = fields.Date("Start Date", required=True)
    end_date = fields.Date("End Date", required=True)
    club_id = fields.Many2one("school.club")
