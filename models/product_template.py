# -*- coding: utf-8 -*-

from odoo import api, fields, models

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
    is_prix_colis          = fields.Float(string='Prix colis', digits='Product Price', compute='_compute_is_prix_colis')

    @api.depends('uom_id', 'is_nb_pieces_par_colis', 'is_poids_net_colis')
    def _compute_is_prix_colis(self):
        for obj in self:
            pricelist = obj._get_contextual_pricelist()
            if pricelist:
                unit_price = pricelist._get_product_price(obj, 1.0, currency=pricelist.currency_id)
            else:
                unit_price = obj.list_price
            qty_colis = obj.is_poids_net_colis if obj.uom_id.name == 'kg' else obj.is_nb_pieces_par_colis
            obj.is_prix_colis = unit_price * qty_colis

    def _get_qty_per_colis(self):
        """Retourne la quantité (pièces ou kg) contenue dans un colis."""
        self.ensure_one()
        return self.is_poids_net_colis if self.uom_id.name == 'kg' else self.is_nb_pieces_par_colis

    def _get_combination_info(self, combination=False, product_id=False, add_qty=1.0, uom_id=False, **kwargs):
        combination_info = super()._get_combination_info(
            combination=combination,
            product_id=product_id,
            add_qty=add_qty,
            uom_id=uom_id,
            **kwargs,
        )
        if self.env.context.get('website_id'):
            qty_per_colis = self._get_qty_per_colis()
            if qty_per_colis:
                for key in ('price', 'list_price'):
                    if combination_info.get(key):
                        combination_info[key] = combination_info[key] * qty_per_colis
        return combination_info

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


