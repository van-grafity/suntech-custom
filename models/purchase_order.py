from odoo import api, fields, models
from odoo.exceptions import RedirectWarning, UserError, ValidationError
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def _get_default_user_id(self):
        return self.env['res.users'].search([('user_id', '=', self.env.uid)], limit=1)

    # department_id = fields.Many2many('hr.department', 'purchase_transaction_rel','id','purchase_id', string='Department', default=lambda self: self.env.user.department_id, readonly=True)

    @api.onchange('partner_id') 
    def _onchange_incoterm_by_supplier(self):
        for this in self:
            this.incoterm_id = this.partner_id.incoterm_id
        print("PO INCOTERM ", this.incoterm_id)

    @api.model
    def create(self, vals):
        res = super(PurchaseOrder, self).create(vals)
        print('xcreate ')
        return res

    def write(self, vals):
        res = super(PurchaseOrder, self).write(vals)
        print('xwrite ')
        return res

    def get_table_purchase(self):
        # date_start = self.date_start.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        # date_end = self.date_end.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        order_obj = self.env['purchase.order']
        docs = order_obj.search([('department_id','=', self.department_id.name)])

        table_purchase = '''
            <center><table class="table table-bordered text-center" style="width:100%">
                <tr style="margin-bottom:20px">
                    <td>PR NO</td>
                    <td>DATE</td>
                    <td>P/O NO</td>
                    <td>SUPPLIER</td>
                    <td>ITEM</td>
                    <td>DO DATE</td>
                    <td>DO NO</td>
                    <td>QTY</td>
                    <td>UNIT</td>
                    <td>CCY</td>
                    <td>PO PRICE</td>
                    <td>TOTAL AMOUNT</td>
                    <td>USAGE</td>
                </tr>
            '''
        
        for models in docs:
            
            table_purchase += '''
                    <tr style="margin-bottom:20px">
                        <td></td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                    '''%(models.date_order, models.name, models.partner_id.name, models.product_id.name)

        print('xTest', table_purchase)

        return table_purchase

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    department_id  = fields.Many2one('hr.department')
    # department_id = fields.Many2many('hr.department', 'po_transaction_rel','id','purchase_id', string='Department', default=lambda self: self.env.user.department_id)

    def get_request_number(self):
        # selected_ids = self.env.context.get('id', [])
        # selected_records = self.env['purchase.order'].browse(selected_ids)
            # where id = %s
        requestObj = self.env['purchase.request']
        count = requestObj.search_count([('id', '=', self.id)])
        
        self.env.cr.execute("""
            select * from purchase_request
        """)
        res = self.env.cr.fetchall()
        print('xRes ', res, '>>>', self.id, '>>>', count)