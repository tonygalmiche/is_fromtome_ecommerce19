# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


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
