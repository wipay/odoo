# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openupgradelib import openupgrade


@openupgrade.logging()
def backup_column_amount(env):
    '''
    Este metodo hace un respaldo de la columna amount en las lineas de depreciacion
    '''
    _columns_backup = {
        'account_asset_depreciation_line': [
            ('amount', None, None), 
        ],
    }
    openupgrade.copy_columns(env.cr, _columns_backup)

@openupgrade.logging()
def add_column_amount_cost(env):
    '''
    Este metodo se encarga de crear la columna amount_cost, en caso que no exista
    '''
    if not openupgrade.column_exists(env.cr, 'account_asset_depreciation_line', 'amount_cost'):
        env.cr.execute('ALTER TABLE "%s" ADD COLUMN "%s" %s' % ('account_asset_depreciation_line', 'amount_cost', 'decimal'))

@openupgrade.logging()
def copy_amount_backup_to_amount_cost(env):
    '''
    Este metodo se encarga de copiar el campo amount_backup al campo amount cost, siempre y cuando no este instalado el modulo ecua_fixed_assets
    '''
    module_ids = env['ir.module.module'].search([('name','=','ecua_fixed_assets'), ('state','=','installed')])
    if not module_ids:
        env.cr.execute('''
            update account_asset_depreciation_line set amount_cost=openupgrade_legacy_10_0_amount
        ''')  
    
@openupgrade.migrate(use_env=True)
def migrate(env, version):
    backup_column_amount(env)
    add_column_amount_cost(env)
    copy_amount_backup_to_amount_cost(env)
    
      