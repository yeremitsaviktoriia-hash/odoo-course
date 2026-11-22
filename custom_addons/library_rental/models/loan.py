from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


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
    due_date = fields.Date(compute='_compute_due_date', store=True, string='Due Date')
    return_date = fields.Date(string='Return Date')
    fine_amount = fields.Float(
        compute='_compute_fine_amount', store=True, string='Fine (UAH)',
    )
    state = fields.Selection(
        [
            ('active', 'Активна'),
            ('returned', 'Повернена'),
        ],
        default='active',
        string='State',
    )
    is_overdue = fields.Boolean(compute='_compute_is_overdue', string='Overdue')

    @api.depends('loan_date')
    def _compute_due_date(self):
        for loan in self:
            loan.due_date = loan.loan_date + timedelta(days=14) if loan.loan_date else False

    @api.depends('due_date', 'return_date')
    def _compute_fine_amount(self):
        for loan in self:
            if loan.due_date and loan.return_date and loan.return_date > loan.due_date:
                overdue_days = (loan.return_date - loan.due_date).days
                loan.fine_amount = overdue_days * 5.0
            else:
                loan.fine_amount = 0.0

    @api.depends('state', 'due_date')
    @api.depends_context('tz', 'uid')
    def _compute_is_overdue(self):
        today = fields.Date.context_today(self)
        for loan in self:
            loan.is_overdue = bool(
                loan.state == 'active' and loan.due_date and loan.due_date < today
            )

    @api.onchange('copy_id')
    def _onchange_copy_id(self):
        if not self.copy_id:
            return

        domain = [('copy_id', '=', self.copy_id.id), ('state', '=', 'active')]
        if self._origin.id:
            domain.append(('id', '!=', self._origin.id))

        if self.search_count(domain, limit=1):
            return {
                'warning': {
                    'title': _('Copy already on loan'),
                    'message': _('This copy already has another active loan.'),
                },
            }

    @api.constrains('copy_id', 'state')
    def _check_unique_active_loan(self):
        for loan in self.filtered(lambda record: record.state == 'active'):
            conflict = self.sudo().search_count([
                ('copy_id', '=', loan.copy_id.id),
                ('state', '=', 'active'),
                ('id', '!=', loan.id),
            ], limit=1)
            if conflict:
                raise ValidationError(_('Цей примірник уже має іншу активну видачу.'))

    @api.constrains('loan_date', 'due_date')
    def _check_due_date(self):
        for loan in self:
            if loan.loan_date and loan.due_date and loan.due_date <= loan.loan_date:
                raise ValidationError(_('Термін повернення має бути пізнішим за дату видачі.'))

    @api.constrains('loan_date', 'return_date')
    def _check_return_date(self):
        for loan in self:
            if loan.loan_date and loan.return_date and loan.return_date < loan.loan_date:
                raise ValidationError(_('Дата повернення не може бути ранішою за дату видачі.'))
