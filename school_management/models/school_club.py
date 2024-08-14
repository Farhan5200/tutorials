# -*- coding: utf-8 -*-

from odoo import fields, models


class SchoolClub(models.Model):
    """used to create club creation form"""
    _name = "school.club"
    _description = "School Club"

    name = fields.Char(string="Name", required=True)
    students_id = fields.Many2many(comodel_name="student.registration")
    event_count = fields.Integer(string="Events", compute="compute_event_count")

    def smart_button(self):
        """action for smart button"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Event',
            'view_mode': 'tree',
            'res_model': 'school.event',
            'domain': [("club_id.name", "=", self.name)]
        }

    def compute_event_count(self):
        """to count number of event in a club"""
        for record in self:
            record.event_count = self.env['school.event'].search_count(
                [('club_id.name', '=', self.name)])
