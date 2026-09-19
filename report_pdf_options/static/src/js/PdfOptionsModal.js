/** @odoo-module */

import { _t } from "@web/core/l10n/translation";
import { Dialog } from "@web/core/dialog/dialog";
import { Component } from "@odoo/owl";

export class PdfOptionsModal extends Component {
    static components = { Dialog };
    static template = "report_pdf_options.ButtonOptions";
    static props = {
        onSelectOption: { type: Function },
        close: { type: Function, optional: true },
    };

    get dialogTitle() {
        return _t("What do you want to do?");
    }
}
