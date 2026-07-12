# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class AssetPortalController(http.Controller):

    @http.route(
        ['/assetflow/portal'],
        type='http',
        auth='user',
        methods=['GET'],
        csrf=False
    )
    def asset_portal(self, **kwargs):

        total_assets = request.env['asset.dashboard'].sudo().search_count([])

        return request.make_response(
            f"AssetFlow Portal Working\nTotal Assets : {total_assets}",
            headers=[('Content-Type', 'text/plain')]
        )