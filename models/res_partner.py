from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"

    incoterm_id = fields.Many2one('account.incoterms', string="Incoterms")