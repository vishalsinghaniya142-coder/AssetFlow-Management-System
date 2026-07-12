# wizard/allocate_asset.py
from odoo import models, fields, api

class AllocateAssetWizard(models.TransientModel):
    _name = 'allocate.asset.wizard'
    _description = 'Allocate Asset Wizard'

    asset_id = fields.Many2one('assetflow.asset', string='Asset', required=True)
    allocation_type = fields.Selection([('employee', 'Employee'), ('department', 'Department')], default='employee', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee')
    department_id = fields.Many2one('hr.department', string='Department')
    expected_return_date = fields.Date(string='Expected Return Date')

    def action_allocate(self):
        self.env['assetflow.allocation'].create({
            'asset_id': self.asset_id.id,
            'allocation_type': self.allocation_type,
            'employee_id': self.employee_id.id,
            'department_id': self.department_id.id,
            'expected_return_date': self.expected_return_date,
        })