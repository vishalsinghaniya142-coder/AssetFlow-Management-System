# -*- coding: utf-8 -*-
"""
Maintenance Wizards
--------------------
1. FacilityMaintenanceScheduleWizard - bulk-create maintenance requests
   across multiple assets in one go (invoked from the Asset list view,
   e.g. select several assets -> Action -> "Schedule Maintenance").

2. FacilityMaintenanceCompleteWizard - captures resolution notes and
   actual cost when closing out a maintenance request, instead of the
   raw `action_done()` writing an empty completion straight away. Gives
   a proper data-entry checkpoint before the record is locked into
   `done` state.

Author : Member 4 (Maintenance, Audit, Reports & Security)
Module : facility_management
"""

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class FacilityMaintenanceScheduleWizard(models.TransientModel):
    """Bulk-schedule maintenance requests for one or more assets."""

    _name = "facility.maintenance.schedule.wizard"
    _description = "Bulk Schedule Maintenance"

    asset_ids = fields.Many2many(
        comodel_name="facility.asset",
        string="Assets",
        required=True,
        help="Assets for which a maintenance request will be created.",
    )

    maintenance_type = fields.Selection(
        selection=[
            ("preventive", "Preventive"),
            ("corrective", "Corrective"),
            ("emergency", "Emergency"),
        ],
        string="Type",
        required=True,
        default="preventive",
    )

    priority = fields.Selection(
        selection=[
            ("0", "Low"),
            ("1", "Normal"),
            ("2", "High"),
            ("3", "Urgent"),
        ],
        string="Priority",
        default="1",
    )

    scheduled_date = fields.Datetime(
        string="Scheduled Date",
        required=True,
        default=fields.Datetime.now,
    )

    technician_id = fields.Many2one(
        comodel_name="res.users",
        string="Assigned Technician",
    )

    downtime_required = fields.Boolean(string="Asset Downtime Required", default=True)

    description = fields.Text(
        string="Description",
        help="Applied identically to every generated maintenance request. "
             "You can edit individual requests afterwards if needed.",
    )

    asset_count = fields.Integer(compute="_compute_asset_count")

    @api.depends("asset_ids")
    def _compute_asset_count(self):
        for wizard in self:
            wizard.asset_count = len(wizard.asset_ids)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_model = self.env.context.get("active_model")
        active_ids = self.env.context.get("active_ids")
        if active_model == "facility.asset" and active_ids:
            res["asset_ids"] = [(6, 0, active_ids)]
        return res

    def action_schedule(self):
        """Create one facility.maintenance record per selected asset."""
        self.ensure_one()
        if not self.asset_ids:
            raise UserError(_("Please select at least one asset."))

        Maintenance = self.env["facility.maintenance"]
        created = Maintenance.browse()
        for asset in self.asset_ids:
            created |= Maintenance.create(
                {
                    "asset_id": asset.id,
                    "maintenance_type": self.maintenance_type,
                    "priority": self.priority,
                    "scheduled_date": self.scheduled_date,
                    "technician_id": self.technician_id.id,
                    "downtime_required": self.downtime_required,
                    "description": self.description,
                }
            )

        # Auto-confirm the freshly created batch so they show up as
        # actionable work rather than sitting in draft.
        created.action_confirm()

        action = self.env["ir.actions.act_window"]._for_xml_id(
            "facility_management.action_facility_maintenance"
        )
        action["domain"] = [("id", "in", created.ids)]
        action["context"] = {}
        return action


class FacilityMaintenanceCompleteWizard(models.TransientModel):
    """Capture resolution details and close out a maintenance request."""

    _name = "facility.maintenance.complete.wizard"
    _description = "Complete Maintenance Request"

    maintenance_id = fields.Many2one(
        comodel_name="facility.maintenance",
        string="Maintenance Request",
        required=True,
        readonly=True,
    )

    resolution_notes = fields.Text(string="Resolution Notes", required=True)
    actual_cost = fields.Monetary(string="Actual Cost", currency_field="currency_id")
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        default=lambda self: self.env.company.currency_id,
    )

    completion_date = fields.Datetime(
        string="Completion Date",
        default=fields.Datetime.now,
        required=True,
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_id = self.env.context.get("active_id")
        if active_id:
            record = self.env["facility.maintenance"].browse(active_id)
            res["maintenance_id"] = record.id
            res["actual_cost"] = record.estimated_cost
        return res

    def action_complete(self):
        self.ensure_one()
        if self.maintenance_id.state != "in_progress":
            raise UserError(
                _("Only requests that are 'In Progress' can be completed through this wizard.")
            )
        self.maintenance_id.write(
            {
                "state": "done",
                "completion_date": self.completion_date,
                "resolution_notes": self.resolution_notes,
                "actual_cost": self.actual_cost,
            }
        )
        return {"type": "ir.actions.act_window_close"}