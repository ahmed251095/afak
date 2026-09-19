"""Drop the leftovers of the custom module `od_exp_hold`.

Its source code is not in this repository (nor in any branch) anymore, so the
module cannot be loaded: it stays in state `to upgrade`, which makes Odoo log
"Some modules have inconsistent states" and, worse, makes the cron runner skip
the whole database ("Skipping database ... because of modules to install/
upgrade/remove"), so no scheduled action runs at all.

All the module still owned was a disabled cron ("EXP.: Hold") calling
`model.del_exp_date_msg()` on res.company -- a method that no longer exists,
which is why that cron already raised AttributeError on 16.0 production.

This runs on every restoration/upgrade build, so the upgraded database is
cleaned the same way on staging and on production.
"""
import logging

_logger = logging.getLogger(__name__)

MODULE = 'od_exp_hold'


def migrate(cr, version):
    cr.execute("SELECT id, state FROM ir_module_module WHERE name = %s", (MODULE,))
    row = cr.fetchone()
    if not row or row[1] == 'uninstalled':
        return
    module_id = row[0]

    cr.execute(
        "SELECT model, res_id FROM ir_model_data WHERE module = %s AND model IN ('ir.cron', 'ir.actions.server')",
        (MODULE,),
    )
    owned = cr.fetchall()
    cron_ids = [res_id for model, res_id in owned if model == 'ir.cron']
    action_ids = [res_id for model, res_id in owned if model == 'ir.actions.server']

    if cron_ids:
        # ir.cron delegates to ir.actions.server, and triggers/progress rows
        # cascade on delete.
        cr.execute("SELECT ir_actions_server_id FROM ir_cron WHERE id IN %s", (tuple(cron_ids),))
        action_ids += [sid for (sid,) in cr.fetchall() if sid]
        cr.execute("DELETE FROM ir_cron WHERE id IN %s", (tuple(cron_ids),))
    if action_ids:
        # ir_act_server inherits the ir_actions table, deleting there is enough
        cr.execute("DELETE FROM ir_act_server WHERE id IN %s", (tuple(set(action_ids)),))

    # The remaining xml ids are duplicates of core records (res.company and its
    # selection values): drop the ownership rows only, never the records.
    cr.execute("DELETE FROM ir_model_data WHERE module = %s", (MODULE,))
    cr.execute(
        "UPDATE ir_module_module SET state = 'uninstalled', latest_version = NULL WHERE id = %s",
        (module_id,),
    )
    _logger.info("Removed the leftovers of the missing module %s", MODULE)
