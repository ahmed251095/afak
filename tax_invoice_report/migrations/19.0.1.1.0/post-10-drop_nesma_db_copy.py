"""Remove the database copy of the "nesma" invoice report.

The report was a UI duplicate of `invoice_customer_report_new` living only in the
database (views `..._new_copy_1` / `request_transfer_layout_custom_copy_1` and an
ir.actions.report named "nesma"). It broke on 19.0 because it still referenced
l10n_sa_delivery_date, and being database-only it could not be fixed by a module
update. The template now lives in report/nesma_invoice_report.xml, so the copies
are dropped here to avoid two "nesma" entries in the print menu.
"""
import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)

OLD_TEMPLATE = 'tax_invoice_report.invoice_customer_report_new_copy_1'
OLD_LAYOUT = 'tax_invoice_report.request_transfer_layout_custom_copy_1'


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})

    # the new report must exist before the old one goes away
    if not env.ref('tax_invoice_report.invoice_report_nesma', raise_if_not_found=False):
        _logger.warning("New nesma report not found, keeping the database copy")
        return

    actions = env['ir.actions.report'].search([('report_name', '=', OLD_TEMPLATE)])
    if actions:
        _logger.info("Removing the database copy of the nesma report action: %s", actions.ids)
        actions.unlink()

    views = env['ir.ui.view'].search([('key', 'in', [OLD_TEMPLATE, OLD_LAYOUT])])
    if views:
        _logger.info("Removing the database copies of the nesma templates: %s", views.ids)
        views.unlink()
