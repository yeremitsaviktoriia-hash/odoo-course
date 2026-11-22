from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    loans = env['library.loan'].search([])
    env.add_to_compute(loans._fields['due_date'], loans)
    loans.flush_recordset(['due_date'])
