# -*- coding: utf-8 -*-
{
    'name': "r_descuento_integrado",

    'summary': """
        Reporte de descuento integrado""",

    'description': """
        Reporte de descuento integrado
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
        'reports/descuento_integrado.xml',
        'views/descuento_integrado_view.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
