{
    'name': 'Sale Task Creator',
    'summary': 'Create tasks directly from the sale order form header',
    'description': """
Adds a button in the sale order form header to create project tasks,
a smart button showing the task count, and an embedded list of
associated tasks in a dedicated notebook page.
    """,
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'author': 'Your Company',
    'website': '',
    'depends': ['sale', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
