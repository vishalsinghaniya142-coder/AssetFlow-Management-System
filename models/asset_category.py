from odoo import models, fields

class AssetCategory(models.Model):
    _name = 'asset.category'
    _description = 'Asset Category'

    name = fields.Char(string="Category Name", required=True)
    code = fields.Char(string="Category Code")
    description = fields.Text(string="Description")