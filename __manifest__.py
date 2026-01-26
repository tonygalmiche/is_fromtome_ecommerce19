# -*- coding: utf-8 -*-
{
    'name'     : 'InfoSaône - Module Odoo 19 de e-commerce pour Fromtome',
    'version'  : '0.1',
    'author'   : 'InfoSaône',
    'category' : 'InfoSaône',
    'description': """
InfoSaône - Module Odoo 19 de e-commerce pour Fromtome
===================================================
""",
    'maintainer' : 'InfoSaône',
    'website'    : 'http://www.infosaone.com',
    'depends'    : [
        'base',
        'product',
        'website_sale',
        'payment',
    ],
    'data' : [
        'views/payment_transaction_views.xml',
    ],
    'installable': True,
    'application': True,
}
