# -*- coding: utf-8 -*-
"""
Maintenance Module
-------------------
Handles preventive & corrective maintenance requests for facility assets.

Author : Member 4 (Maintenance, Audit, Reports & Security)
Module : facility_management

NOTE:
    - `facility.asset`  -> placeholder for the Asset model built by Member 1/2.
    - `facility.booking` -> placeholder for the Booking model built by Member 2/3.
    Update the `comodel_name` in the Many2one fields below once the actual
    technical model names are finalized by the respective owners.
"""

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class FacilityMaintenance(models.Model):
    """Represents a single maintenance request/job raised against an asset."""

    _name = "facility.maintenance"
    _description = "Facility Maintenance Request"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "scheduled_date desc, id desc"
    _rec_name = "name"

    # ------------------------------------------------------------------
    # Basic Fields
    # ------------------------------------------------------------------
    name = fields.Char(
        string="Reference",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _("New"),
        tracking=True,
    )

    asset_id = fields.Many2one(
        comodel_name="facility.asset",
        string="Asset",
        required=True,
        ondelete="restrict",
        tracking=True,
        index=True,
        help="Asset on which this maintenance is being performed.",
    )

    booking_id = fields.Many2one(
        comodel_name="facility.booking",
        string="Related Booking",
        ondelete="set null",
        help="If maintenance was triggered by / blocks a specific booking.",
    )

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )

    active = fields.Boolean(default=True)

    # ------------------------------------------------------------------
    # Classification
    # ------------------------------------------------------------------
    maintenance_type = fields.Selection(
        selection=[
            ("preventive", "Preventive"),
            ("corrective", "Corrective"),
            ("emergency", "Emergency"),
        ],
        string="Type",
        required=True,
        default="corrective",
        tracking=True,
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
        tracking=True,
    )

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("in_progress", "In Progress"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="draft",
        required=True,
        tracking=True,
        copy=False,
    )

    # ------------------------------------------------------------------
    # People
    # ------------------------------------------------------------------
    technician_id = fields.Many2one(
        comodel_name="res.users",
        string="Assigned Technician",
        tracking=True,
        default=lambda self: self.env.user,
    )

    requested_by = fields.Many2one(
        comodel_name="res.users",
        string="Requested By",
        default=lambda self: self.env.user,
        readonly=True,
    )

    # ------------------------------------------------------------------
    # Dates
    # ------------------------------------------------------------------
    request_date = fields.Datetime(
        string="Request Date",
        default=fields.Datetime.now,
        required=True,
    )

    scheduled_date = fields.Datetime(
        string="Scheduled Date",
        tracking=True,
        help="Planned date/time for the maintenance to begin.",
    )

    start_date = fields.Datetime(string="Actual Start", readonly=True, copy=False)
    completion_date = fields.Datetime(string="Actual Completion", readonly=True, copy=False)

    duration_hours = fields.Float(
        string="Duration (Hours)",
        compute="_compute_duration_hours",
        store=True,
        help="Actual time taken, computed from start to completion.",
    )

    is_overdue = fields.Boolean(
        string="Overdue",
        compute="_compute_is_overdue",
        search="_search_is_overdue",
    )

    # ------------------------------------------------------------------
    # Cost & Description
    # ------------------------------------------------------------------
    description = fields.Text(string="Issue / Work Description")
    resolution_notes = fields.Text(string="Resolution Notes")

    estimated_cost = fields.Monetary(string="Estimated Cost", currency_field="currency_id")
    actual_cost = fields.Monetary(string="Actual Cost", currency_field="currency_id")

    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id,
    )

    downtime_required = fields.Boolean(
        string="Asset Downtime Required",
        default=True,
        help="If checked, the asset will be marked unavailable for booking "
             "while this maintenance is in progress.",
    )

    # ------------------------------------------------------------------
    # Compute / Search Methods
    # ------------------------------------------------------------------
    @api.depends("start_date", "completion_date")
    def _compute_duration_hours(self):
        for rec in self:
            if rec.start_date and rec.completion_date:
                delta = rec.completion_date - rec.start_date
                rec.duration_hours = round(delta.total_seconds() / 3600.0, 2)
            else:
                rec.duration_hours = 0.0

    @api.depends("scheduled_date", "state")
    def _compute_is_overdue(self):
        now = fields.Datetime.now()
        for rec in self:
            rec.is_overdue = bool(
                rec.scheduled_date
                and rec.scheduled_date < now
                and rec.state in ("draft", "confirmed")
            )

    def _search_is_overdue(self, operator, value):
        now = fields.Datetime.now()
        if (operator == "=" and value) or (operator == "!=" and not value):
            return [
                ("scheduled_date", "<", now),
                ("state", "in", ("draft", "confirmed")),
            ]
        return [
            "|",
            ("scheduled_date", ">=", now),
            ("state", "not in", ("draft", "confirmed")),
        ]

    # ------------------------------------------------------------------
    # Constraints
    # ------------------------------------------------------------------
    @api.constrains("scheduled_date", "request_date")
    def _check_scheduled_date(self):
        for rec in self:
            if rec.scheduled_date and rec.request_date and rec.scheduled_date < rec.request_date:
                raise ValidationError(
                    _("Scheduled date cannot be earlier than the request date.")
                )

    @api.constrains("start_date", "completion_date")
    def _check_completion_after_start(self):
        for rec in self:
            if rec.start_date and rec.completion_date and rec.completion_date < rec.start_date:
                raise ValidationError(
                    _("Completion date cannot be earlier than the start date.")
                )

    _sql_constraints = [
        (
            "estimated_cost_positive",
            "CHECK(estimated_cost >= 0)",
            "Estimated cost cannot be negative.",
        ),
        (
            "actual_cost_positive",
            "CHECK(actual_cost >= 0)",
            "Actual cost cannot be negative.",
        ),
    ]

    # ------------------------------------------------------------------
    # CRUD Overrides
    # ------------------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("New")) == _("New"):
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "facility.maintenance"
                ) or _("New")
        return super().create(vals_list)

    # ------------------------------------------------------------------
    # State Transition Actions
    # ------------------------------------------------------------------
    def action_confirm(self):
        for rec in self:
            if rec.state != "draft":
                raise UserError(_("Only draft requests can be confirmed."))
        self.write({"state": "confirmed"})

    def action_start(self):
        for rec in self:
            if rec.state != "confirmed":
                raise UserError(_("Only confirmed requests can be started."))
        self.write({"state": "in_progress", "start_date": fields.Datetime.now()})

    def action_done(self):
        for rec in self:
            if rec.state != "in_progress":
                raise UserError(_("Only in-progress requests can be marked done."))
        self.write({"state": "done", "completion_date": fields.Datetime.now()})

    def action_cancel(self):
        for rec in self:
            if rec.state == "done":
                raise UserError(_("A completed maintenance request cannot be cancelled."))
        self.write({"state": "cancelled"})

    def action_reset_to_draft(self):
        self.write(
            {
                "state": "draft",
                "start_date": False,
                "completion_date": False,
            }
        )


class FacilityMaintenanceSchedule(models.Model):
    """Recurring preventive maintenance schedule, used by a scheduled cron
    (see data/cron_jobs.xml) to auto-generate `facility.maintenance` records.
    """

    _name = "facility.maintenance.schedule"
    _description = "Preventive Maintenance Schedule"
    _order = "next_date asc"

    name = fields.Char(required=True)
    asset_id = fields.Many2one(
        comodel_name="facility.asset",
        string="Asset",
        required=True,
        ondelete="cascade",
    )
    interval_number = fields.Integer(string="Repeat Every", default=1, required=True)
    interval_type = fields.Selection(
        selection=[("days", "Day(s)"), ("weeks", "Week(s)"), ("months", "Month(s)")],
        default="months",
        required=True,
    )
    next_date = fields.Date(string="Next Due Date", required=True)
    active = fields.Boolean(default=True)
    responsible_id = fields.Many2one(comodel_name="res.users", string="Responsible")
    note = fields.Text(string="Instructions")

    def _create_maintenance_request(self):
        """Called by cron job to generate the next maintenance request
        and roll `next_date` forward."""
        MaintenanceRequest = self.env["facility.maintenance"]
        for schedule in self:
            MaintenanceRequest.create(
                {
                    "asset_id": schedule.asset_id.id,
                    "maintenance_type": "preventive",
                    "scheduled_date": schedule.next_date,
                    "technician_id": schedule.responsible_id.id,
                    "description": schedule.note or _(
                        "Auto-generated preventive maintenance."
                    ),
                }
            )
            schedule.next_date = fields.Date.add(
                schedule.next_date,
                **{schedule.interval_type: schedule.interval_number},
            )