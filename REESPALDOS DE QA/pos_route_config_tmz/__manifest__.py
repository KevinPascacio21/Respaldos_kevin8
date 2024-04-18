# -*- coding: utf-8 -*-
{
    'name': "pos_route_config_tmz",

    'summary': """
        Manage POS unit session""",

    'description': """
        Manage a POS unit weight and other data before opening or closing a session
    """,

    'author': "Kevin",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'report_xlsx'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'reports/pos_route_config.xml',
        'views/pos_route_config_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
