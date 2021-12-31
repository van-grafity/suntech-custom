from odoo import fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT

class SuntechPurchaseDepartmentWizard(models.TransientModel):
    _name = 'suntech.purchase.department.wizard'

    department_id = fields.Many2one('hr.department', string="Department")
    date_start = fields.Date()
    date_end = fields.Date()

    def _get_order_obj(self):
        order_obj = self.env['purchase.order']
        count = order_obj.search_count([('department_id','=', self.department_id.name)])
        print('xCount ', count)
        return order_obj

    def print_purchase_department(self):
        
        date_start = self.date_start.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        date_end = self.date_end.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        print('xStart', date_start, 'End ', date_end)
        docs = self._get_order_obj().search([('department_id','=', self.department_id.name), ('date_order', '>=', date_start), ('date_order', '<=', date_end)])
        
        if docs:
            print('xPurchaseDepartment ', docs)
        else:
            raise UserError(_("Date range not found"))

        return self.env.ref('suntech_custom.action_report_pr_per_po').report_action(docs)
    
