# -*- coding: utf-8 -*-

from odoo import fields, models


class AssetFlowSettings(models.TransientModel):
    _inherit = "res.config.settings"

    # Dashboard Settings
    dashboard_enabled = fields.Boolean(
        string="Enable Dashboard",
        config_parameter="assetflow.dashboard_enabled",
        default=True,
    )

    show_dashboard_statistics = fields.Boolean(
        string="Show Dashboard Statistics",
        config_parameter="assetflow.show_dashboard_statistics",
        default=True,
    )

    # API Settings
    allow_api_access = fields.Boolean(
        string="Enable REST API",
        config_parameter="assetflow.allow_api_access",
        default=True,
    )

    # Portal Settings
    allow_portal_access = fields.Boolean(
        string="Enable Portal Access",
        config_parameter="assetflow.allow_portal_access",
        default=True,
    )

    # Asset Settings
    auto_generate_asset_code = fields.Boolean(
        string="Auto Generate Asset Code",
        config_parameter="assetflow.auto_generate_asset_code",
        default=True,
    )

    default_asset_category = fields.Selection(
        [
            ("hardware", "Hardware"),
            ("software", "Software"),
            ("furniture", "Furniture"),
            ("vehicle", "Vehicle"),
            ("other", "Other"),
        ],
        string="Default Asset Category",
        config_parameter="assetflow.default_asset_category",
        default="hardware",
    )

    maintenance_notification_days = fields.Integer(
        string="Maintenance Reminder (Days)",
        config_parameter="assetflow.maintenance_notification_days",
        default=30,
    )

    company_name = fields.Char(
        string="Company Name",
        config_parameter="assetflow.company_name",
    )

    company_email = fields.Char(
        string="Company Email",
        config_parameter="assetflow.company_email",
    )

    company_phone = fields.Char(
        string="Company Phone",
        config_parameter="assetflow.company_phone",
    )

    company_address = fields.Text(
        string="Company Address",
        config_parameter="assetflow.company_address",
    )