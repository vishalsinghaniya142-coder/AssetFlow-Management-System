# wizard/return_asset.py
from odoo import models, fields, api

class ReturnAssetWizard(models.TransientModel):
    _name = 'return.asset.wizard'
    _description = 'Return Asset Wizard'

    allocation_id = fields.Many2one('assetflow.allocation', string='Allocation', required=True)
    notes = fields.Text(string='Condition Check-in Notes', required=True)

    def action_return(self):
        self.allocation_id.write({
            'state': 'returned',
            'actual_return_date': fields.Date.context_today(self),
            'notes': self.notes
        })
        self.allocation_id.asset_id.write({'status': 'Available'})