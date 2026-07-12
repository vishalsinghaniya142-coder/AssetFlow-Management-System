from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AssetFlowTransfer(models.Model):
    _name = 'assetflow.transfer'
    _description = 'Asset Transfer Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Transfer Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    asset_id = fields.Many2one('assetflow.asset', string='Asset', required=True, tracking=True)
    current_allocation_id = fields.Many2one('assetflow.allocation', string='Current Allocation', readonly=True)
    
    current_holder = fields.Char(string='Current Holder', compute='_compute_current_holder')
    
    target_type = fields.Selection([
        ('employee', 'Employee'),
        ('department', 'Department')
    ], string='Transfer To', default='employee', required=True)
    
    target_employee_id = fields.Many2one('hr.employee', string='Target Employee')
    target_department_id = fields.Many2one('hr.department', string='Target Department')
    
    reason = fields.Text(string='Reason for Transfer', required=True)
    state = fields.Selection([
        ('draft', 'Requested'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft', tracking=True)

    @api.depends('asset_id')
    def _compute_current_holder(self):
        for record in self:
            active_alloc = self.env['assetflow.allocation'].search([
                ('asset_id', '=', record.asset_id.id),
                ('state', '=', 'active')
            ], limit=1)
            if active_alloc:
                record.current_allocation_id = active_alloc.id
                record.current_holder = active_alloc.employee_id.name if active_alloc.allocation_type == 'employee' else active_alloc.department_id.name
            else:
                record.current_holder = "Unknown / Available"

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('assetflow.transfer') or _('New')
        return super(AssetFlowTransfer, self).create(vals)

    def action_approve(self):
        for record in self:
            if record.current_allocation_id:
                record.current_allocation_id.write({'state': 'transferred', 'actual_return_date': fields.Date.context_today(self)})
            
            # Create the new allocation automatically
            self.env['assetflow.allocation'].create({
                'asset_id': record.asset_id.id,
                'allocation_type': record.target_type,
                'employee_id': record.target_employee_id.id if record.target_type == 'employee' else False,
                'department_id': record.target_department_id.id if record.target_type == 'department' else False,
                'state': 'active'
            })
            record.write({'state': 'approved'})
            
    def action_reject(self):
        self.write({'state': 'rejected'})