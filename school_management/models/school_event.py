# -*- coding: utf-8 -*-

from odoo import fields, models


class SchoolEvent(models.Model):
    """to create event creation form"""
    _name = "school.event"
    _description = "School Event"
    _inherit = 'mail.thread'

    name = fields.Char("Name", required=True, tracking=True)
    start_date = fields.Date("Start Date", required=True)
    end_date = fields.Date("End Date", required=True)
    club_id = fields.Many2many("school.club")
    status = fields.Selection([
        ('start', 'Start'),
        ('ongoing', 'Ongoing'),
        ('cancel', 'Cancel')],
        tracking=True
    )
    internal_notes = fields.Html()
