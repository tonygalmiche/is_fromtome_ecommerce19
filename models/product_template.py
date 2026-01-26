# -*- coding: utf-8 -*-

from odoo import models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _filter_products_with_pricelist_price(self):
        """
        Filtre les produits dont le prix selon la liste de prix actuelle est supérieur à 0.
        Retourne un recordset des produits visibles.
        """
        if not self:
            return self
        
        # Récupérer la pricelist contextuelle (du site web)
        pricelist = self._get_contextual_pricelist()
        if not pricelist:
            # Fallback: retourner tous les produits si pas de pricelist
            return self
        
        visible_products = self.env['product.template']
        
        for product in self:
            # Calculer le prix selon la pricelist
            price = pricelist._get_product_price(
                product,
                1.0,
                currency=pricelist.currency_id,
            )
            if price > 0:
                visible_products |= product
        
        return visible_products


