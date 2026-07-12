# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import date

class TestMaintenance(TransactionCase):

    def setUp(self):
        super(TestMaintenance, self).setUp()
        # Create test data
        self.asset = self.env['asset.asset'].create({
            'name': 'Test Laptop',
            'category_id': self.env.ref('asset_management.asset_category_computer').id,  # adjust ref as per your module
        })

        self.maintenance = self.env['maintenance.request'].create({
            'name': 'MNT-TEST-001',
            'asset_id': self.asset.id,
            'request_date': date.today(),
            'description': 'Screen not working properly',
            'state': 'draft',
        })

    def test_maintenance_creation(self):
        """Test creation of maintenance request"""
        self.assertEqual(self.maintenance.name, 'MNT-TEST-001')
        self.assertEqual(self.maintenance.state, 'draft')
        self.assertEqual(self.maintenance.description, 'Screen not working properly')

    def test_state_transition(self):
        """Test state changes in maintenance workflow"""
        self.maintenance.action_request()
        self.assertEqual(self.maintenance.state, 'requested')

        self.maintenance.action_approve()
        self.assertEqual(self.maintenance.state, 'approved')

    def test_audit_log_creation(self):
        """Test audit log entry on maintenance change"""
        audit_count_before = self.env['audit.log'].search_count([])
        self.maintenance.description = "Updated description"
        audit_count_after = self.env['audit.log'].search_count([])
        self.assertGreater(audit_count_after, audit_count_before)

    def test_report_generation(self):
        """Test maintenance report action"""
        report_action = self.env.ref('member4_maintenance.action_report_maintenance')
        self.assertTrue(report_action)
        # You can further test report rendering if needed

if __name__ == '__main__':
    # For running tests
    pass

