from odoo import models, fields

class Employee(models.Model):
    _name = 'asset.employee'
    _description = 'Employee'

    name = fields.Char(string="Employee Name", required=True)
    employee_id = fields.Char(string="Employee ID")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")

    department_id = fields.Many2one(
        'asset.department',
        string="Department"
    )