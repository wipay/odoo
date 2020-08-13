# -*- coding: utf-8 -*-
from openupgradelib import openupgrade

@openupgrade.logging()
def delete_asset_id_from_account_move_line(env):
    """
    elimina los datos del campo asset_id en la tabla 
    account_move_line sacando una copia primero
    """
    # Sacamos el respaldo de la columna
    openupgrade.copy_columns({'account_move_line':[('asset_id', None, None)]})
    # vaciamos la columna
    openupgrade.logged_query(env.cr, "update account_move_line set asset_id is NULL")


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    delete_asset_id_from_account_move_line(env)