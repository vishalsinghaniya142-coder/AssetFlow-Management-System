from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AssetFlowAllocation(models.Model):
    _name = 'assetflow.allocation'
    _description = 'Asset Allocation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Allocation Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    asset_id = fields.Many2one('assetflow.asset', string='Asset', required=True, tracking=True, domain=[('status', '=', 'Available')])
    allocation_type = fields.Selection([
        ('employee', 'Employee'),
        ('department', 'Department')
    ], string='Allocation Type', default='employee', required=True, tracking=True)
    
    employee_id = fields.Many2one('hr.employee', string='Employee', tracking=True)
    department_id = fields.Many2one('hr.department', string='Department', tracking=True)
    
    allocation_date = fields.Date(string='Allocation Date', default=fields.Date.context_today, required=True)
    expected_return_date = fields.Date(string='Expected Return Date', tracking=True)
    actual_return_date = fields.Date(string='Actual Return Date', readonly=True)
    
    state = fields.Selection([
        ('active', 'Active'),
        ('returned', 'Returned'),
        ('transferred', 'Transferred')
    ], string='Status', default='active', tracking=True, readonly=True)
    
    notes = fields.Text(string='Condition Check-in/Notes')
    is_overdue = fields.Boolean(string='Is Overdue', compute='_compute_is_overdue', store=True)

    @api.depends('expected_return_date', 'state')
    def _compute_is_overdue(self):
        today = fields.Date.context_today(self)
        for record in self:
            if record.state == 'active' and record.expected_return_date and record.expected_return_date < today:
                record.is_overdue = True
            else:
                record.is_overdue = False

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('assetflow.allocation') or _('New')
        
        # Double allocation guard
        asset = self.env['assetflow.asset'].browse(vals.get('asset_id'))
        if asset.status != 'Available':
            raise ValidationError(_("Conflict: This asset is currently not available or already held!"))
            
        record = super(AssetFlowAllocation, self).create(vals)
        asset.write({'status': 'Allocated'})
        return record

    def action_return_asset(self):
        """ Direct fallback route """
        for record in self:
            record.write({
                'state': 'returned',
                'actual_return_date': fields.Date.context_today(self)
            })
            record.asset_id.write({'status': 'Available'})

    @api.model
    def check_and_notify_overdue_allocations(self):
        """ Yeh function cron job run karega automated alerts generate karne ke liye """
        today = fields.Date.context_today(self)
        overdue_records = self.search([
            ('state', '=', 'active'),
            ('expected_return_date', '<', today)
        ])
        
        for record in overdue_records:
            record.is_overdue = True
            
            # Recipient find karna (Employee ka user account)
            recipient_user = record.employee_id.user_id if record.employee_id else False
            if recipient_user:
                self.env['assetflow.notification'].create({
                    'title': f'Overdue Alert: {record.asset_id.name}',
                    'message': f'Dear {record.employee_id.name}, the asset {record.asset_id.name} allocated to you was supposed to be returned by {record.expected_return_date}. Please return or renew it immediately.',
                    'notification_type': 'overdue',
                    'user_id': recipient_user.id,
                    'is_read': False
                })