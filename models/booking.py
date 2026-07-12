from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AssetFlowBooking(models.Model):
    _name = 'assetflow.booking'
    _description = 'Resource Booking'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Booking Reference', required=True, readonly=True, default=lambda self: _('New'))
    asset_id = fields.Many2one('assetflow.asset', string='Resource/Asset', required=True, domain=[('is_shared_bookable', '=', True)])
    employee_id = fields.Many2one('hr.employee', string='Booked By', default=lambda self: self.env.user.employee_id.id, required=True)
    
    start_datetime = fields.Datetime(string='Start Time', required=True, tracking=True)
    end_datetime = fields.Datetime(string='End Time', required=True, tracking=True)
    
    state = fields.Selection([
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='upcoming', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('assetflow.booking') or _('New')
        
        self._validate_overlapping_bookings(vals.get('asset_id'), vals.get('start_datetime'), vals.get('end_datetime'))
        return super(AssetFlowBooking, self).create(vals)

    def write(self, vals):
        for record in self:
            asset_id = vals.get('asset_id', record.asset_id.id)
            start = vals.get('start_datetime', record.start_datetime)
            end = vals.get('end_datetime', record.end_datetime)
            if 'asset_id' in vals or 'start_datetime' in vals or 'end_datetime' in vals:
                record._validate_overlapping_bookings(asset_id, start, end, exclude_id=record.id)
        return super(AssetFlowBooking, self).write(vals)

    def _validate_overlapping_bookings(self, asset_id, start, end, exclude_id=False):
        if start >= end:
            raise ValidationError(_("Start Time must be strictly before End Time."))
            
        domain = [
            ('asset_id', '=', asset_id),
            ('state', 'not in', ['cancelled']),
            ('start_datetime', '<', end),
            ('end_datetime', '>', start)
        ]
        if exclude_id:
            domain.append(('id', '!=', exclude_id))
            
        overlapping = self.search(domain)
        if overlapping:
            raise ValidationError(_("Overlap detected! This resource is already booked for the selected timeframe."))

    def action_complete(self):
        self.write({'state': 'completed'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})