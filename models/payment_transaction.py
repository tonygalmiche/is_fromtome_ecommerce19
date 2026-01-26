# -*- coding: utf-8 -*-

from odoo import models, _
from odoo.exceptions import UserError


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def action_set_done(self):
        """
        Action pour passer manuellement une transaction à l'état 'done'.
        Utilisé pour les paiements par virement bancaire validés manuellement.
        """
        for tx in self:
            if tx.state == 'pending':
                tx._set_done()
            elif tx.state == 'done':
                raise UserError(_("Cette transaction est déjà confirmée."))
            else:
                raise UserError(_("Seules les transactions en attente peuvent être confirmées. État actuel : %s") % tx.state)
        return True

    def action_set_canceled(self):
        """
        Action pour annuler manuellement une transaction.
        """
        for tx in self:
            if tx.state in ('pending', 'draft'):
                tx._set_canceled()
            elif tx.state == 'cancel':
                raise UserError(_("Cette transaction est déjà annulée."))
            else:
                raise UserError(_("Cette transaction ne peut pas être annulée. État actuel : %s") % tx.state)
        return True
