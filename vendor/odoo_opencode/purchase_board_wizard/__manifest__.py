{
    'name': 'Purchase Board Wizard',
    'version': '19.0.1.0.0',
    'category': 'Purchase',
    'summary': 'Wizard to add board products with format area to purchase orders',
    'description': """
Adds a wizard accessible from the Purchase Order form header to select a board product,
its format (with predefined area), and quantity. Validates that the product UoM is m²
and creates a purchase order line with the calculated total area.
    """,
    'author': 'Your Company',
    'website': '',
    'depends': ['purchase', 'uom'],
    'data': [
        'security/ir.model.access.csv',
        'views/board_format_views.xml',
        'views/purchase_order_line_views.xml',
        'views/purchase_board_wizard_views.xml',
        'views/purchase_order_views.xml',
    ],
    'demo': [
        'data/board_format_data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}