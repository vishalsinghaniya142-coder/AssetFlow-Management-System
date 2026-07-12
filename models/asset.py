from odoo import models, fields

class Asset(models.Model):
    _name = 'asset.asset'
    _description = 'Asset'

    name = fields.Char(string="Asset Name", required=True)
    asset_code = fields.Char(string="Asset Code")

    employee_id = fields.Many2one(
        'asset.employee',
        string="Assigned Employee"
    )

    department_id = fields.Many2one(
        'asset.department',
        string="Department"
    )

    category_id = fields.Many2one(
        'asset.category',
        string="Category"
    )

    purchase_date = fields.Date(string="Purchase Date")

    status = fields.Selection([
        ('available', 'Available'),
        ('assigned', 'Assigned'),
        ('maintenance', 'Maintenance'),
    ], string="Status", default='available')