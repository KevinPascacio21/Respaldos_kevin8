# -*- coding: utf-8 -*-
{
    'name': "POS Route config",

    'summary': """
        Manage POS unit session
        """,

    'description': """
        Manage a POS unit weight and other data before opening or closing a session
    """,

    'author': "Hipólito Rodríguez, Sergio Segovia",
    'website': "gazready-test.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'point_of_sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'point_of_sale', 'hr'],

    'qweb': [
        'static/src/xml/field.xml'
    ],

    # always loaded
    'data': [
        'data/data.xml',   
        'data/sequence.xml',   
        'reports/pos_route_config.xml',
        'security/ir.model.access.csv',     
        'security/security.xml',
        'views/pos_route_config_view.xml',#k
        #'views/setting.xml',
        'views/menu.xml' # Se debe agregar al final para que no falle la instalación
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

