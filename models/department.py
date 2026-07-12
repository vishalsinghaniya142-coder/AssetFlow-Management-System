from odoo import models, fields

class Department(models.Model):
    _name = 'asset.department'
    _description = 'Department'

    name = fields.Char(string="Department Name", required=True)
    code = fields.Char(string="Department Code")
    description = fields.Text(string="Description")