from odoo import fields, models


class LibraryLoan(models.Model):
    _name = 'library.loan'
    _description = 'Library Book Loan'

    copy_id = fields.Many2one(
        'library.copy',
        required=True,
        ondelete='restrict',
        string='Copy',
    )
    member_id = fields.Many2one(
        'library.member',
        required=True,
        ondelete='restrict',
        string='Member',
    )
    book_name = fields.Char(related='copy_id.book_id.name', string='Book')
    book_author = fields.Char(related='copy_id.book_id.author', string='Author')
    membership_number = fields.Char(
        related='member_id.membership_number',
        string='Membership Number',
    )
    loan_date = fields.Date(default=fields.Date.context_today, string='Loan Date')
    due_date = fields.Date(string='Due Date')
    return_date = fields.Date(string='Return Date')
    state = fields.Selection(
        [
            ('active', 'Активна'),
            ('returned', 'Повернена'),
        ],
        default='active',
        string='State',
    )
