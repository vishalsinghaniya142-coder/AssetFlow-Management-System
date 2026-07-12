# wizard/booking_wizard.py
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class BookingWizard(models.TransientModel):
    _name = 'booking.wizard'
    _description = 'Create Resource Booking Wizard'

    asset_id = fields.Many2one('assetflow.asset', string='Resource/Asset', required=True, domain=[('is_shared_bookable', '=', True)])
    employee_id = fields.Many2one('hr.employee', string='Booked By', default=lambda self: self.env.user.employee_id.id, required=True)
    start_datetime = fields.Datetime(string='Start Time', required=True)
    end_datetime = fields.Datetime(string='End Time', required=True)

    @api.model
    def default_get(self, fields_list):
        """ Agar hum asset form se button click karke kholenge, 
            toh yeh automatically asset select kar lega """
        res = super(BookingWizard, self).default_get(fields_list)
        if self.env.context.get('active_model') == 'assetflow.asset':
            res['asset_id'] = self.env.context.get('active_id')
        return res

    def action_confirm_booking(self):
        self.ensure_one()
        
        # Yeh line actual model 'assetflow.booking' me record insert karegi
        # Aur overlap validation ka logic jo humne main model me likha hai, woh auto-trigger ho jayega!
        self.env['assetflow.booking'].create({
            'asset_id': self.asset_id.id,
            'employee_id': self.employee_id.id,
            'start_datetime': self.start_datetime,
            'end_datetime': self.end_datetime,
            'state': 'upcoming',
        })
        return {'type': 'ir.actions.act_window_close'}