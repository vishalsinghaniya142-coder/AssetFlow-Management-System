# -*- coding: utf-8 -*-

from odoo import http


class AssetDashboardController(http.Controller):

    @http.route('/assetflow', auth='user', type='http')
    def dashboard(self, **kwargs):
        return http.Response(
            "AssetFlow Dashboard Controller Working",
            status=200
        )