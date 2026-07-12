from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class TestAssetFlowBooking(TransactionCase):

    def setUp(self):
        super(TestAssetFlowBooking, self).setUp()
        # Find or mock essential models
        self.asset_bookable = self.env['assetflow.asset'].create({
            'name': 'Conference Room A',
            'is_shared_bookable': True,
            'status': 'Available'
        })
        self.employee = self.env['hr.employee'].create({'name': 'Yash Srivastava'})

    def test_overlapping_booking_fails(self):
        start = datetime.now() + timedelta(days=1)
        end = start + timedelta(hours=2)
        
        # Create initial valid slot
        self.env['assetflow.booking'].create({
            'asset_id': self.asset_bookable.id,
            'employee_id': self.employee.id,
            'start_datetime': start,
            'end_datetime': end,
        })

        # Attempt overlapping slot creation
        with self.assertRaises(ValidationError):
            self.env['assetflow.booking'].create({
                'asset_id': self.asset_bookable.id,
                'employee_id': self.employee.id,
                'start_datetime': start + timedelta(hours=1),
                'end_datetime': end + timedelta(hours=1),
            })