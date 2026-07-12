# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import json


class AssetDashboardAPI(http.Controller):

    @http.route(
        '/api/assets',
        auth='user',
        type='http',
        methods=['GET'],
        csrf=False
    )
    def get_assets(self, **kwargs):

        assets = request.env['asset.dashboard'].sudo().search([])

        result = []

        for asset in assets:
            result.append({
                "id": asset.id,
                "asset_name": asset.asset_name,
                "asset_code": asset.asset_code,
                "category": asset.category,
                "owner": asset.owner,
                "department": asset.department,
                "purchase_date": str(asset.purchase_date),
                "purchase_cost": asset.purchase_cost,
                "status": asset.status,
            })

        return request.make_response(
            json.dumps({
                "status": "success",
                "count": len(result),
                "data": result
            }),
            headers=[
                ('Content-Type', 'application/json')
            ]
        )


    @http.route(
        '/api/dashboard/stats',
        auth='user',
        type='json',
        methods=['POST'],
        csrf=False
    )
    def dashboard_stats(self):

        Asset = request.env['asset.dashboard'].sudo()

        return {
            "total_assets": Asset.search_count([]),
            "available": Asset.search_count([('status', '=', 'available')]),
            "assigned": Asset.search_count([('status', '=', 'assigned')]),
            "maintenance": Asset.search_count([('status', '=', 'maintenance')]),
            "retired": Asset.search_count([('status', '=', 'retired')]),
        }