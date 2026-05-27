/** @odoo-module **/

import { patch } from '@web/core/utils/patch';
import { redirect } from '@web/core/utils/urls';
import { WebsiteSale } from '@website_sale/interactions/website_sale';
import wSaleUtils from '@website_sale/js/website_sale_utils';

/**
 * Extension du comportement de filtrage de la boutique en ligne pour supporter
 * les 4 filtres personnalisés Fromtome :
 * - region_ids       : Many2one is.region.origine
 * - type_article_ids : Many2one is.type.article
 * - traitement_thermique : Selection
 * - famille_fromage_ids  : Many2one is.famille.fromage
 */
patch(WebsiteSale.prototype, {

    /**
     * @override
     * Gère les checkboxes des filtres Fromtome en plus des filtres standard
     * (attribute_value, tags).
     */
    onChangeAttribute(ev) {
        const IS_FILTER_NAMES = new Set([
            'region_ids',
            'type_article_ids',
            'traitement_thermique',
            'famille_fromage_ids',
        ]);

        // Vérifier si l'élément modifié est l'un de nos filtres
        const isFromtomeFilter = IS_FILTER_NAMES.has(ev.currentTarget.name);

        if (!isFromtomeFilter) {
            // Déléguer au comportement standard pour les filtres attribute_value et tags
            return super.onChangeAttribute(ev);
        }

        // Traitement pour nos filtres personnalisés
        const productGrid = this.el.querySelector('.o_wsale_products_grid_table_wrapper');
        if (productGrid) {
            productGrid.classList.add('opacity-50');
        }

        const form = wSaleUtils.getClosestProductForm(ev.currentTarget);
        const filters = form.querySelectorAll('input:checked, select');

        const attributeValues = new Map();
        const tags = new Set();
        const regionIds = new Set();
        const typeArticleIds = new Set();
        const traitementThermique = new Set();
        const familleFromageIds = new Set();

        for (const filter of filters) {
            if (filter.value) {
                switch (filter.name) {
                    case 'attribute_value': {
                        const [attributeId, attributeValueId] = filter.value.split('-');
                        const valueIds = attributeValues.get(attributeId) ?? new Set();
                        valueIds.add(attributeValueId);
                        attributeValues.set(attributeId, valueIds);
                        break;
                    }
                    case 'tags':
                        tags.add(filter.value);
                        break;
                    case 'region_ids':
                        regionIds.add(filter.value);
                        break;
                    case 'type_article_ids':
                        typeArticleIds.add(filter.value);
                        break;
                    case 'traitement_thermique':
                        traitementThermique.add(filter.value);
                        break;
                    case 'famille_fromage_ids':
                        familleFromageIds.add(filter.value);
                        break;
                }
            }
        }

        const url = new URL(form.action);
        const searchParams = url.searchParams;

        // Paramètres standard
        for (const entry of attributeValues.entries()) {
            searchParams.append('attribute_values', `${entry[0]}-${[...entry[1]].join(',')}`);
        }
        if (tags.size) {
            searchParams.set('tags', [...tags].join(','));
        }

        // Paramètres Fromtome (multi-value)
        for (const id of regionIds) {
            searchParams.append('region_ids', id);
        }
        for (const id of typeArticleIds) {
            searchParams.append('type_article_ids', id);
        }
        for (const val of traitementThermique) {
            searchParams.append('traitement_thermique', val);
        }
        for (const id of familleFromageIds) {
            searchParams.append('famille_fromage_ids', id);
        }

        redirect(`${url.pathname}?${searchParams.toString()}`);
    },
});
