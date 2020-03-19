# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    asset_depreciation_ids = fields.One2many('account.asset.depreciation.line', 'move_id', string='Assets Depreciation Lines', ondelete="restrict")

    @api.multi
    def button_cancel(self):
        for move in self:
            #Codigo moldificado por Trescloud pues usuarios contables que no tienen acceso
            #al modulo de activos no le permite aprobar o anular fact, nc, pagos, etc, por
            #tal motivo se agrega el sudo()
            for line in move.sudo().asset_depreciation_ids:
                line.move_posted_check = False
        return super(AccountMove, self).button_cancel()

    @api.multi
    def post(self):
        for move in self:
            #Codigo moldificado por Trescloud pues usuarios contables que no tienen acceso
            #al modulo de activos no le permite aprobar o anular fact, nc, pagos, etc, por
            #tal motivo se agrega el sudo()
            for depreciation_line in move.sudo().asset_depreciation_ids:
                depreciation_line.post_lines_and_close_asset()
        return super(AccountMove, self).post()
