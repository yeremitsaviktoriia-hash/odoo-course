from odoo import fields, models


class LibraryCopy(models.Model):
    _name = 'library.copy'
    _description = 'Library Book Copy'
    _rec_name = 'inventory_number'

    book_id = fields.Many2one(
        'library.book',
        required=True,
        ondelete='restrict',
        string='Book',
    )
    inventory_number = fields.Char(required=True, string='Inventory Number')
    condition = fields.Selection(
        [
            ('new', 'Новий'),
            ('good', 'Добрий'),
            ('damaged', 'Пошкоджений'),
        ],
        default='good',
        string='Condition',
    )
    loan_ids = fields.One2many('library.loan', 'copy_id', string='Loans')
