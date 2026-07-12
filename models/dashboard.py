# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AssetDashboard(models.Model):
    _name = "asset.dashboard"
    _description = "Asset Dashboard"
    _rec_name = "asset_name"
    _order = "create_date desc"

    _sql_constraints = [
        (
            "asset_code_unique",
            "unique(asset_code)",
            "Asset Code must be unique!"
        ),
    ]

    asset_name = fields.Char(
        string="Asset Name",
        required=True,
        tracking=True
    )

    asset_code = fields.Char(
        string="Asset Code",
        required=True,
        copy=False,
        readonly=True,
        tracking=True
    )

    category = fields.Selection(
        [
            ("hardware", "Hardware"),
            ("software", "Software"),
            ("furniture", "Furniture"),
            ("vehicle", "Vehicle"),
            ("other", "Other"),
        ],
        string="Category",
        default="hardware",
        required=True,
    )

    owner = fields.Char(string="Owner")

    department = fields.Char(string="Department")

    purchase_date = fields.Date(string="Purchase Date")

    purchase_cost = fields.Float(string="Purchase Cost")

    status = fields.Selection(
        [
            ("available", "Available"),
            ("assigned", "Assigned"),
            ("maintenance", "Maintenance"),
            ("retired", "Retired"),
        ],
        string="Status",
        default="available",
        tracking=True,
    )

    description = fields.Text(string="Description")

    active = fields.Boolean(default=True)

    @api.constrains("purchase_cost")
    def _check_purchase_cost(self):
        for rec in self:
            if rec.purchase_cost < 0:
                raise ValidationError(
                    "Purchase Cost cannot be negative."
                )

    @api.model
    def create(self, vals):

        if not vals.get("asset_code"):

            total = self.search_count([]) + 1

            vals["asset_code"] = f"AST-{total:04d}"

        return super().create(vals)

    def action_mark_available(self):
        self.write({"status": "available"})
        return True

    def action_mark_assigned(self):
        self.write({"status": "assigned"})
        return True

    def action_mark_maintenance(self):
        self.write({"status": "maintenance"})
        return True

    def action_retire(self):
        self.write({"status": "retired"})
        return True

    @api.model
    def get_dashboard_data(self):

        return {
            "total_assets": self.search_count([]),
            "available_assets": self.search_count(
                [("status", "=", "available")]
            ),
            "assigned_assets": self.search_count(
                [("status", "=", "assigned")]
            ),
            "maintenance_assets": self.search_count(
                [("status", "=", "maintenance")]
            ),
            "retired_assets": self.search_count(
                [("status", "=", "retired")]
            ),
        }