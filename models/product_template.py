# -*- coding: utf-8 -*-

from odoo import fields, models

_COLISAGE = [
    ('1', 'Colis'),
    ('2', '1/2 colis'),
    ('4', '1/4 colis'),
]


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_colisage            = fields.Selection(string='Colisage', selection=_COLISAGE, required=True, tracking=True, default='1', help="Utilisé dans 'Préparation transfert entrepôt'")
    is_nb_pieces_par_colis = fields.Integer(string='Nb Pièces / colis', tracking=True)
    is_poids_net_colis     = fields.Float(string='Poids net colis (Kg)', digits='Stock Weight', tracking=True)

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


