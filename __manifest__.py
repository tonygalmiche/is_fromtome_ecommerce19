# -*- coding: utf-8 -*-
{
    'name'     : 'InfoSaône - Module Odoo 19 de e-commerce pour Fromtome',
    'version'  : '0.1',
    'author'   : 'InfoSaône',
    'category' : 'InfoSaône',
    'description': """
InfoSaône - Module Odoo 19 de e-commerce pour Fromtome
=======================================================
""",
    'maintainer' : 'InfoSaône',
    'website'    : 'http://www.infosaone.com',
    'depends'    : [
        'base',
        'product',
        'uom',
        'website_sale',
        'payment',
    ],
    'data' : [
        'security/ir.model.access.csv',
        'views/payment_transaction_views.xml',
        'views/product_template_views.xml',
    ],
    "assets": {
        "web.assets_backend": [
            "is_fromtome_ecommerce19/static/src/scss/**/*",
        ],
        "web.assets_frontend": [
            "is_fromtome_ecommerce19/static/src/js/nb_colis.js",
            "is_fromtome_ecommerce19/static/src/scss/website_sale.scss",
        ],
    },
    'license'     : 'LGPL-3',
    'installable' : True,
    'application' : True,
}
