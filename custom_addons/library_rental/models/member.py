from odoo import fields, models


class LibraryMember(models.Model):
    _name = 'library.member'
    _description = 'Library Member'

    _membership_number_unique = models.Constraint(
        'UNIQUE (membership_number)',
        'Membership number must be unique.',
    )

    name = fields.Char(required=True)
    membership_number = fields.Char(required=True)
    email = fields.Char()
    phone = fields.Char()
    loan_ids = fields.One2many('library.loan', 'member_id', string='Loans')
