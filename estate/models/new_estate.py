from odoo import models, fields


class Estate(models.Model):
    _name = "new.estate"
    _description = "new estate"

    name = fields.Char("Title", required=True)
    description = fields.Text("Description")
    post_code = fields.Char("Postcode")
    expected_price = fields.Float("Expected Price", required=True)
    bedrooms = fields.Integer("Bedrooms", required=True, default=2)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    living_area = fields.Integer('Living Area(sqm)')
    availability_date = fields.Date("Available From", required=True, copy=False, default=fields.Datetime.now)
    active = fields.Boolean('Active', default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer Received', 'Offer Received'),
        ('offer accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ], required=True, copy=False, default='new')
