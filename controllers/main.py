# -*- coding: utf-8 -*-

from odoo import fields, http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.controllers.cart import Cart
from odoo.addons.payment import utils as payment_utils


class CartFromtome(Cart):

    @http.route()
    def update_cart(self, line_id, quantity, product_id=None, **kwargs):
        order_sudo = request.cart
        IrUiView = request.env['ir.ui.view']

        if not line_id:
            line_id = order_sudo.order_line.filtered(
                lambda sol: sol.product_id.id == product_id
            )[:1].id

        # Autoriser les flottants si l'UdM a une précision inférieure à 1
        line = order_sudo.order_line.filtered(lambda l: l.id == line_id)[:1]
        if line and line.product_id.uom_id.rounding < 1.0:
            quantity = float(quantity)
        else:
            quantity = int(quantity)

        values = order_sudo._cart_update_line_quantity(line_id, quantity, **kwargs)

        values['cart_quantity'] = order_sudo.cart_quantity
        values['cart_ready'] = order_sudo._is_cart_ready()
        values['amount'] = order_sudo.amount_total
        values['minor_amount'] = (
            order_sudo and payment_utils.to_minor_currency_units(
                order_sudo.amount_total, order_sudo.currency_id
            )
        ) or 0.0
        values['website_sale.cart_lines'] = IrUiView._render_template(
            'website_sale.cart_lines', {
                'website_sale_order': order_sudo,
                'date': fields.Date.today(),
                'suggested_products': order_sudo._cart_accessories(),
            }
        )
        values['website_sale.total'] = IrUiView._render_template(
            'website_sale.total', {
                'website_sale_order': order_sudo,
            }
        )
        values['website_sale.quick_reorder_history'] = IrUiView._render_template(
            'website_sale.quick_reorder_history', {
                'website_sale_order': order_sudo,
                **self._prepare_order_history(),
            }
        )
        return values


class WebsiteSaleFromtome(WebsiteSale):

    def _shop_lookup_products(self, options, post, search, website):
        """
        Surcharge pour filtrer les produits dont le prix selon la liste de prix 
        est supérieur à 0 pour les utilisateurs non internes (portail/public).
        """
        fuzzy_search_term, product_count, search_result = super()._shop_lookup_products(
            options, post, search, website
        )
        
        # Appliquer le filtre uniquement pour les utilisateurs non internes
        if not request.env.user._is_internal():
            # Filtrer les produits avec un prix > 0 selon la pricelist
            search_result = search_result._filter_products_with_pricelist_price()
            product_count = len(search_result)
        
        return fuzzy_search_term, product_count, search_result
