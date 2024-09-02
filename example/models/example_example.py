from odoo import fields, models

class ExampleExample(models.Model):
    _name = "example.example"

    name=fields.Char("Name")
    partner_id = fields.Many2one("res.partner","Customer")
    tag_ids = fields.Many2many("example.tag", string="Example Tags")
    line_ids = fields.One2many("example.line", 'example_example_id', string="Example line")
