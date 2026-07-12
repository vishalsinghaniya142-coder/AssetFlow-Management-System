# -*- coding: utf-8 -*-

from odoo import api, fields, models


class AssetDashboard(models.Model):
    _name = "asset.dashboard"
    _description = "Asset Dashboard"
    _rec_name = "asset_name"
    _order = "create_date desc"

    asset_name = fields.Char(
        string="Asset Name",
        required=True
    )

    asset_code = fields.Char(
        string="Asset Code",
        required=True,
        copy=False
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

    owner = fields.Char(
        string="Owner"
    )

    department = fields.Char(
        string="Department"
    )

    purchase_date = fields.Date(
        string="Purchase Date"
    )

    purchase_cost = fields.Float(
        string="Purchase Cost"
    )

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

    description = fields.Text(
        string="Description"
    )

    active = fields.Boolean(
        default=True
    )

    @api.model
    def create(self, vals):
        """
        Automatically generate Asset Code.
        """

        if not vals.get("asset_code"):
            count = self.search_count([]) + 1
            vals["asset_code"] = f"AST-{count:04d}"

        return super().create(vals)

    def action_mark_assigned(self):
        for record in self:
            record.status = "assigned"

    def action_mark_available(self):
        for record in self:
            record.status = "available"

    def action_mark_maintenance(self):
        for record in self:
            record.status = "maintenance"

    def action_retire(self):
        for record in self:
            record.status = "retired"

    def get_dashboard_data(self):
        """
        Dashboard Statistics
        """

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