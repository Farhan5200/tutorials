from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    total_line_price = fields.Float(compute="_compute_total_line_price", string="Total Cost")

    @api.depends('product_uom_qty', 'product_id', 'quantity')
    def _compute_total_line_price(self):
        for rec in self:
            if rec.product_id.supplier_taxes_id.amount:
                rec.total_line_price = rec.product_id.standard_price * rec.quantity * (
                            (rec.product_id.supplier_taxes_id.amount + 100) / 100)
            else:
                rec.total_line_price = rec.product_id.standard_price * rec.quantity


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    total_price_components = fields.Float(compute="_compute_total_price_components", string="Total Cost")
    extra_cost_during_manu_ids = fields.One2many('reason.extra', 'linked_manu_order_id')

    @api.depends('move_raw_ids', 'extra_cost_during_manu_ids')
    def _compute_total_price_components(self):
        for rec in self:
            total_amount = 0
            for records in rec.move_raw_ids:
                total_amount += records.total_line_price
            if rec.extra_cost_during_manu_ids:
                for records in rec.extra_cost_during_manu_ids:
                    total_amount += records.price
            rec.total_price_components = total_amount

    def create_bill(self):
        bill = self.env['account.move'].create({
            'move_type': 'in_invoice',
        })
        for rec in self.move_raw_ids:
            if rec.picked:
                bill.update({
                    'invoice_line_ids': [fields.Command.create({
                        'product_id': rec.product_id.id,
                        'quantity': rec.quantity,
                    })]
                })
        if self.extra_cost_during_manu_ids:
            for rec in self.extra_cost_during_manu_ids:
                bill.update({
                    'invoice_line_ids': [fields.Command.create({
                        'name': rec.reason,
                        'price_unit': rec.price,
                    })]
                })

        # lines=[]
        # for rec in self.move_raw_ids:
        #     if rec.picked:
        #         line_values={
        #             'product_id':rec.product_id.id,
        #             'quantity': rec.quantity,
        #         }
        #         lines.append(fields.Command.create(line_values))
        # if self.extra_cost_during_manu_ids:
        #     for rec in self.extra_cost_during_manu_ids:
        #         extra_values={
        #             'name': rec.reason,
        #             'price_unit':rec.price,
        #         }
        #         lines.append(fields.Command.create(extra_values))
        # bill.create({
        #     'move_type': 'in_invoice',
        #     'invoice_line_ids': lines
        # })


class ReasonExtra(models.Model):
    _name = "reason.extra"

    reason = fields.Char(string="Description", required=True)
    price = fields.Float(string="price")
    linked_manu_order_id = fields.Many2one('mrp.production')
