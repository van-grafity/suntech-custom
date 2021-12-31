from odoo import api, fields, models
from odoo.exceptions import RedirectWarning, UserError, ValidationError

from datetime import date
from datetime import datetime
from datetime import datetime, timedelta

from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
from email.utils import formataddr

class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'

    remark = fields.Text(string="Remark", required=True)
    is_users = fields.Boolean(default='True', compute='_compute_who_user_has_groups')
    user_id = fields.Many2one(comodel_name='res.users', string='User', track_visibility='onchange', readonly=True, 
                      states={'draft': [('readonly', False)]}, default=lambda self: self.env.user)
    dept_id = fields.Many2one('hr.department', string="Department", default=lambda self: self.env.user.department_id)

    # order_id = fields.Many2one('purchase.order')

    def _get_employee(self):
        resource = self.env['resource.resource'].search([('user_id','=',self.env.user.id)])
        employee = self.env['hr.employee'].search([('resource_id','=',resource.id)])
        return employee.department_id.head_department_id
         
    employee_id = fields.Many2one(comodel_name='hr.employee', string="Head Department", readonly=True, store=True, default=_get_employee)
    
    def _get_today(self):
        res = datetime.today()
        return res

    datett_start = fields.Datetime(default=_get_today)

    @api.model
    def create(self, vals):
        res = super(PurchaseRequest, self).create(vals)
      
        print("xxcreate ")
        return res

    def write(self, vals):
        res = super(PurchaseRequest, self).write(vals)
        # if self.env.user.has_group('base.group_user'):
        #     base_group = self.env.ref('base.group_user')
        #     raise ValidationError('Only user with this access rights (%s) are allowed to ....' % base_group.name)
        print('xwrite ')
        return res

    def _compute_who_user_has_groups(self):
        print("xIs user ?")
        if self.env.user.has_group('suntech_custom.group_suntech_super_users_admin'):
            self.is_users = True
            print("xuser The User belongs to an Salesman Group")
        else:
            self.is_users = False
            print("xuser Whoops! User does not belong to this Group")

    def send_share_by_mail(self, template_xmlid):
        self.ensure_one()
        request_template = self.env.ref(template_xmlid, raise_if_not_found=False)
        if request_template:
            mail = request_template.with_context(user_id=self.create_uid.id).send_mail(self.id)
            self.env['mail.mail'].browse(mail).send()

    def _get_request_obj(self):
        pr_obj = self.env['purchase.request']
        count = pr_obj.search_count([('state','=', "to_approve")])
        print('xCount ', count)
        return pr_obj

    def _get_config_base_url(self):
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        return base_url
    
    def _get_request_action_id(self):
        action_id = self.env.ref('purchase_request.purchase_request_form_action', raise_if_not_found=False)
        return action_id

    def _provide_mail_template(self):
        docs = self._get_request_obj().search([('state','=', "to_approve")])
        print('xDocs ', self.date_start, ">>> ",docs, ">>> ", self._get_today())
        item = []
        table_data_html = ""
        regex_link = ""
        for rec in docs:
            print('xTest ', rec.date_start)
            print('xcreate ', self.datett_start)
            regex_link = str(self._get_config_base_url()) + "/web#id=" + str(rec.id) + "&amp;action=" + str(self._get_request_action_id().id) + "&amp;model=purchase.request&amp;view_type=form"
            item.append({
                'name' : rec.name,
                'link' : regex_link,
            })

        for line in item:
            button = """
                <a href = "{}"
                    style="background-color: #3c509a; min-width: 60px; display: inline-block; text-align: center; padding: 10px 30px 10px 30px; text-decoration: none; color: #fff; border-radius: 5px; font-size:13px;">
                    View
                </a>
            """.format(line['link'])
            table_data_html += """<tr>
                <td style="border: 1px solid black; padding: 2px;">{}</td>
                <td style="border: 1px solid black; padding: 2px;">{}</td>
            </tr>""".format(line['name'],button)

        body_html = """ <p>
                            Hi,
                            <br/><br/>
                            We see that a request has not been approved for acceptance in the system. 
                            <br></br>
                            Please look at the request.
                            <br></br>
                            If the request has been seen, please click the “Approve” button to set the status of the request as accepted in the system.
                            <br/><br/>
                        </p>
                    <table style="border-collapse:collapse;">
                        <thead>
                            <tr>
                            </tr>
                        </thead>
                        <tbody>
                            <td valign="top" style="font-size: 13px; width: 70%;">{}</td>
                        </tbody>
                    </table>
                    <br>
                    <br>
                    This email is auto generated by the system, please do not reply to this email.
            """.format(table_data_html)
        subject = ("""PR Reminder""")
        company = self.env.company

        mails = {
            'subject' : subject,
            'email_from': formataddr((company.name, company.email)),
            'email_to': 'vanlaserblack@gmail.com',
            'reply_to': 'noreply-mail.com',
            'body_html': body_html,
            'auto_delete': False,
        }
        mail = self.env['mail.mail'].create(mails)
        return mail
    
    def _cron_remind_purchase_request(self):
        date_start = self._get_today() + timedelta(hours=+24)
        date_start = date_start.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        date_end = self._get_today()
        date_end = date_end.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        print("xx ",date_end, " === ", date_start)
        print('xx2 ', date_start)
        
        docs = self._get_request_obj().search([('date_start','>=', date_start), ('date_start','<=', date_end)])
        # for item in docs:
        #     if item:
        #         if date_start == date_end:
        self._provide_mail_template().send()