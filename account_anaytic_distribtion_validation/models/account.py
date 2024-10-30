from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AccountAccount(models.Model):
    _inherit = 'account.account'

    analytic_distribution_required = fields.Boolean(
        string="Require Analytic Distribution",
        help="If enabled, analytic distribution will be required on account move lines."
    )


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.constrains('account_id', 'analytic_distribution')
    def _check_analytic_distribution(self):
        for line in self:
            if line.account_id.analytic_distribution_required and not line.analytic_distribution:
                raise ValidationError("Analytic distribution is required for account '%s'." % line.account_id.display_name)