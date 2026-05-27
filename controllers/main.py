# -*- coding: utf-8 -*-

from odoo import fields, http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.controllers.cart import Cart
from odoo.addons.payment import utils as payment_utils

_TRAITEMENT_THERMIQUE_LABELS = {
    'laitcru': 'Lait Cru',
    'laitthermise': 'Lait Thermisé',
    'laitpasteurisé': 'Lait Pasteurisé',
}


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

    def _shop_get_query_url_kwargs(self, search, min_price, max_price, order=None, tags=None, **kwargs):
        res = super()._shop_get_query_url_kwargs(search, min_price, max_price, order=order, tags=tags, **kwargs)
        args = request.httprequest.args
        res.update({
            'region_ids': args.getlist('region_ids'),
            'type_article_ids': args.getlist('type_article_ids'),
            'traitement_thermique': args.getlist('traitement_thermique'),
            'famille_fromage_ids': args.getlist('famille_fromage_ids'),
        })
        return res

    def _get_search_options(self, category=None, attribute_value_dict=None, tags=None,
                            min_price=0.0, max_price=0.0, conversion_rate=1, **post):
        res = super()._get_search_options(
            category=category, attribute_value_dict=attribute_value_dict, tags=tags,
            min_price=min_price, max_price=max_price, conversion_rate=conversion_rate, **post
        )
        args = request.httprequest.args
        res.update({
            'region_ids': [int(x) for x in args.getlist('region_ids') if x],
            'type_article_ids': [int(x) for x in args.getlist('type_article_ids') if x],
            'traitement_thermique': [x for x in args.getlist('traitement_thermique') if x],
            'famille_fromage_ids': [int(x) for x in args.getlist('famille_fromage_ids') if x],
        })
        return res

    def _get_additional_shop_values(self, values, **kwargs):
        res = super()._get_additional_shop_values(values, **kwargs)
        env = request.env
        args = request.httprequest.args

        active_region_ids = [int(x) for x in args.getlist('region_ids') if x]
        active_type_article_ids = [int(x) for x in args.getlist('type_article_ids') if x]
        active_traitement = [x for x in args.getlist('traitement_thermique') if x]
        active_famille_ids = [int(x) for x in args.getlist('famille_fromage_ids') if x]

        res.update({
            'all_regions': env['is.region.origine'].sudo().search([]),
            'all_types_article': env['is.type.article'].sudo().search([]),
            'all_familles_fromage': env['is.famille.fromage'].sudo().search([]),
            'traitement_thermique_options': list(_TRAITEMENT_THERMIQUE_LABELS.items()),
            'active_region_ids': active_region_ids,
            'active_type_article_ids': active_type_article_ids,
            'active_traitement_thermique': active_traitement,
            'active_famille_fromage_ids': active_famille_ids,
        })
        return res
