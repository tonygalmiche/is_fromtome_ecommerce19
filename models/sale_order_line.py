# -*- coding: utf-8 -*-

from odoo import models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _get_display_price(self):
        price = super()._get_display_price()
        qty_per_colis = self.product_id.product_tmpl_id._get_qty_per_colis()
        if qty_per_colis:
            price = price * qty_per_colis
        return price
