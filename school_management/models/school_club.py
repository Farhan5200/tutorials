# -*- coding: utf-8 -*-

from odoo import fields, models


class SchoolClub(models.Model):
    """used to create club creation form"""
    _name = "school.club"
    _description = "School Club"
    _inherit = 'mail.thread'

    name = fields.Char(string="Name", required=True, tracking=True)
    students_ids = fields.Many2many(comodel_name="student.registration")
    event_count = fields.Integer(string="Events", compute="_compute_event_count")
    color = fields.Integer(string="Color")
    school_id = fields.Many2one("res.company", string="School", tracking=True,
                                default=lambda self: self.env.company)

    def get_events(self):
        """action for smart button"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Event',
            'view_mode': 'tree',
            'res_model': 'school.event',
            'domain': [("club_ids.name", "=", self.name)],
            'context': "{'create': False}"
        }

    def _compute_event_count(self):
        """to count number of event in a club"""
        for record in self:
            record.event_count = self.env['school.event'].search_count(
                [('club_ids', '=', record.id)])
