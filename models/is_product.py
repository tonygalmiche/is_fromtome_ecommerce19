# -*- coding: utf-8 -*-

from odoo import fields, models


class IsRegionOrigine(models.Model):
    _name = "is.region.origine"
    _description = "Région d'origine"
    _order = "name"

    name = fields.Char("Région d'origine", required=True)


class IsFamilleFromage(models.Model):
    _name = "is.famille.fromage"
    _description = "Famille de fromage"
    _order = "name"

    name = fields.Char("Famille de fromage", required=True)


class IsTypeArticle(models.Model):
    _name = "is.type.article"
    _description = "Type article"
    _order = "name"

    name = fields.Char("Type article", required=True)
