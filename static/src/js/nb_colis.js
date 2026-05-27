/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

// Fiche produit : quand l'utilisateur change la quantite (= nb colis),
// affiche dynamiquement l'equivalent "soit X pieces/kg" a cote du selecteur.
publicWidget.registry.IsNbColis = publicWidget.Widget.extend({
    selector: "#product_detail",
    events: {
        "change input[name=add_qty]": "_onQtyChange",
    },

    start() {
        this._super(...arguments);
        this._updateDisplay();
    },

    _onQtyChange() {
        this._updateDisplay();
    },

    _updateDisplay() {
        const $span = this.$(".is_qty_colis_display");
        if (!$span.length) return;
        const qty = parseFloat(this.$("input[name=add_qty]").val()) || 1;
        const qtyPerColis = parseFloat($span.data("qty-per-colis")) || 1;
        const uom = $span.data("uom") || "";
        const total = qty * qtyPerColis;
        const totalStr = Number.isInteger(total) ? String(total) : total.toFixed(2);
        $span.text("Colis soit " + totalStr + " " + uom);
    },
});
