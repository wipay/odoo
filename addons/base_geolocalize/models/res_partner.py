# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
import urllib2

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError

# INICIO DEL CODIGO MODIFICADO POR TRESCLOUD
def geo_find(addr, google_maps_api_key=False):
# FIN DEL CODIGO MODIFICADO POR TRESCLOUD
    if not addr:
        return None
    url = 'https://maps.googleapis.com/maps/api/geocode/json?sensor=false&address='
    url += urllib2.quote(addr.encode('utf8'))
    # INICIO DEL CODIGO AGREGADO POR TRESCLOUD
    if google_maps_api_key:
        url += '&key=%s' % google_maps_api_key
    # FIN DEL CODIGO AGREGADO POR TRESCLOUD

    try:
        result = json.load(urllib2.urlopen(url))
    except Exception as e:
        raise UserError(_('Cannot contact geolocation servers. Please make sure that your Internet connection is up and running (%s).') % e)

    if result['status'] != 'OK':
        return None

    try:
        geo = result['results'][0]['geometry']['location']
        return float(geo['lat']), float(geo['lng'])
    except (KeyError, ValueError):
        return None


def geo_query_address(street=None, zip=None, city=None, state=None, country=None):
    if country and ',' in country and (country.endswith(' of') or country.endswith(' of the')):
        # put country qualifier in front, otherwise GMap gives wrong results,
        # e.g. 'Congo, Democratic Republic of the' => 'Democratic Republic of the Congo'
        country = '{1} {0}'.format(*country.split(',', 1))
    return tools.ustr(', '.join(filter(None, [street,
                                              ("%s %s" % (zip or '', city or '')).strip(),
                                              state,
                                              country])))


class ResPartner(models.Model):
    _inherit = "res.partner"

    partner_latitude = fields.Float(string='Geo Latitude', digits=(16, 5))
    partner_longitude = fields.Float(string='Geo Longitude', digits=(16, 5))
    date_localization = fields.Date(string='Geolocation Date')

    @api.multi
    def geo_localize(self):
        # INICIO DEL CODIGO AGREGADO POR TRESCLOUD
        google_maps_api_key = self.env[
            'ir.config_parameter'
        ].sudo().get_param('google_maps_api_key')
        # FIN DEL CODIGO AGREGADO POR TRESCLOUD
        # We need country names in English below
        for partner in self.with_context(lang='en_US'):
            # INICIO DEL CODIGO MODIFICADO POR TRESCLOUD
            result = geo_find(geo_query_address(street=partner.street,
                                                zip=partner.zip,
                                                city=partner.city,
                                                state=partner.state_id.name,
                                                country=partner.country_id.name),
                              google_maps_api_key)
            # FIN DEL CODIGO MODIFICADO POR TRESCLOUD
            if result is None:
                # INICIO DEL CODIGO MODIFICADO POR TRESCLOUD
                result = geo_find(geo_query_address(
                    city=partner.city,
                    state=partner.state_id.name,
                    country=partner.country_id.name
                ), google_maps_api_key)
                # FIN DEL CODIGO MODIFICADO POR TRESCLOUD

            if result:
                partner.write({
                    'partner_latitude': result[0],
                    'partner_longitude': result[1],
                    'date_localization': fields.Date.context_today(partner)
                })
        return True
