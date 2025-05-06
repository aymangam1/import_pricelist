# -*- coding: utf-8 -*-
{
    'name': 'Import Pricelist from Excel',
    'version': '1.0',
    'depends': ['product', 'sale'],
    'category': 'Sales',
    'summary': 'Import product prices from Excel to Pricelist',
    'data': [
        'security/ir.model.access.csv',
        'wizard/import_wizard_view.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
    'author': "Ayman Gamal",
}


