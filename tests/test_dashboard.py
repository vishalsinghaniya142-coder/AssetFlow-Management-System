# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase


class TestAssetDashboard(TransactionCase):

    def setUp(self):
        super().setUp()

        self.Asset = self.env['asset.dashboard']

        self.asset = self.Asset.create({
            'asset_name': 'Laptop',
            'asset_code': 'AST-0001',
            'category': 'hardware',
            'owner': 'Admin',
            'department': 'IT',
            'purchase_cost': 50000,
            'status': 'available',
        })

    def test_asset_creation(self):
        """Test asset creation"""

        self.assertTrue(self.asset)
        self.assertEqual(self.asset.asset_name, 'Laptop')
        self.assertEqual(self.asset.status, 'available')

    def test_asset_status_change(self):
        """Test status update"""

        self.asset.write({
            'status': 'assigned'
        })

        self.assertEqual(
            self.asset.status,
            'assigned'
        )

    def test_dashboard_statistics(self):
        """Test dashboard statistics"""

        total_assets = self.Asset.search_count([])

        self.assertGreaterEqual(
            total_assets,
            1
        )

    def test_asset_delete(self):
        """Test delete asset"""

        self.asset.unlink()

        self.assertEqual(
            self.Asset.search_count([]),
            0
        )