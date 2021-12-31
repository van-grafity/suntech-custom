# -*- coding: utf-8 -*-
{
    'name': 'Suntech Custom',
    'category': 'Uncategorized', 
    'author': 'SGEEDE', 
    'version': '1.0',
    'website': 'https://www.sgeede.com',
    'summary': 'Custom Module',
    'description': """
Suntech Custom Module
""",
    'depends': ['base', 'mail', 'purchase_request'],
    'data': [
        'security/ir.model.access.csv',
        'security/suntech_security.xml',
        'data/suntech_cron.xml',
        'data/mail_templates.xml',

        'wizard/suntech_purchase_department_wizard.xml',
        'wizard/purchase_request_line_make_purchase_order_view.xml',

        'views/suntech_main_view.xml',

        'report/multiple_po_per_pr_report.xml',
        'report/suntech_pr_per_po.xml',
        

        
    ],
    'qweb': [
        # "static/src/xml/*.xml",
    ],
}

