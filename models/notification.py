from odoo import models, fields, api

class AssetFlowNotification(models.Model):
    _name = 'assetflow.notification'
    _description = 'AssetFlow System Notification'
    _order = 'create_date desc'

    title = fields.Char(string='Title', required=True)
    message = fields.Text(string='Message', required=True)
    notification_type = fields.Selection([
        ('allocation', 'Allocation'),
        ('transfer', 'Transfer'),
        ('booking', 'Booking'),
        ('overdue', 'Overdue Alert')
    ], string='Type', required=True)
    user_id = fields.Many2one('res.users', string='Recipient', required=True)
    is_read = fields.Boolean(string='Read', default=False)