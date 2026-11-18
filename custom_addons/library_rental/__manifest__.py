{
    'name': 'Library Rental',
    'version': '19.0.1.0.0',
    'category': 'Services',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/book_views.xml',
        'views/copy_views.xml',
        'views/member_views.xml',
        'views/loan_views.xml',
    ],
    'demo': [
        'demo/library_demo.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}
