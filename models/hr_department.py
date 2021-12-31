from odoo import api, fields, models

class HrDepartment(models.Model):
    _inherit = "hr.department"

    head_department_id = fields.Many2one('hr.employee', string="Head Department")