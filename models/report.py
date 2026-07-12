# -*- coding: utf-8 -*-
"""
Report Module
-------------
Contains:
  1. QWeb report "parser" models (AbstractModel, `report.<module>.<report_name>`)
     that supply computed data to the printable PDF templates defined under
     report/asset_report.xml, report/booking_report.xml,
     report/maintenance_report.xml, report/audit_report.xml.
  2. `facility.report.dashboard` - a lightweight aggregator model that
     computes KPI summaries (counts, costs, overdue items, trends) consumed
     by report/dashboard_report.xml and any dashboard view/widget.

Author : Member 4 (Maintenance, Audit, Reports & Security)
Module : facility_management

NOTE:
    `facility.asset` and `facility.booking` are placeholders for the models
    owned by Member 1/2/3 - update comodel_name / search domains once the
    real technical names are confirmed.
"""

from datetime import timedelta

from odoo import api, fields, models, _


# =========================================================================
# QWeb Report Parsers
# =========================================================================
class MaintenanceReportParser(models.AbstractModel):
    """Feeds report/maintenance_report.xml (ir.actions.report -> QWeb)."""

    _name = "report.facility_management.report_maintenance_document"
    _description = "Maintenance Report Parser"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env["facility.maintenance"].browse(docids)
        return {
            "doc_ids": docids,
            "doc_model": "facility.maintenance",
            "docs": docs,
            "total_cost": sum(docs.mapped("actual_cost")),
            "generated_on": fields.Datetime.now(),
            "generated_by": self.env.user.name,
        }


class AssetReportParser(models.AbstractModel):
    """Feeds report/asset_report.xml."""

    _name = "report.facility_management.report_asset_document"
    _description = "Asset Report Parser"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env["facility.asset"].browse(docids)
        Maintenance = self.env["facility.maintenance"]

        asset_maintenance_summary = {}
        for asset in docs:
            requests = Maintenance.search([("asset_id", "=", asset.id)])
            asset_maintenance_summary[asset.id] = {
                "total_requests": len(requests),
                "open_requests": len(requests.filtered(lambda r: r.state not in ("done", "cancelled"))),
                "total_maintenance_cost": sum(requests.mapped("actual_cost")),
            }

        return {
            "doc_ids": docids,
            "doc_model": "facility.asset",
            "docs": docs,
            "maintenance_summary": asset_maintenance_summary,
            "generated_on": fields.Datetime.now(),
            "generated_by": self.env.user.name,
        }


class BookingReportParser(models.AbstractModel):
    """Feeds report/booking_report.xml."""

    _name = "report.facility_management.report_booking_document"
    _description = "Booking Report Parser"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env["facility.booking"].browse(docids)
        return {
            "doc_ids": docids,
            "doc_model": "facility.booking",
            "docs": docs,
            "generated_on": fields.Datetime.now(),
            "generated_by": self.env.user.name,
        }


class AuditReportParser(models.AbstractModel):
    """Feeds report/audit_report.xml. Typically run over a date range /
    model filter rather than a single record id, so `data` (passed in from
    the triggering wizard/action) carries the filter criteria."""

    _name = "report.facility_management.report_audit_document"
    _description = "Audit Report Parser"

    @api.model
    def _get_report_values(self, docids, data=None):
        data = data or {}
        domain = []

        if data.get("date_from"):
            domain.append(("create_date", ">=", data["date_from"]))
        if data.get("date_to"):
            domain.append(("create_date", "<=", data["date_to"]))
        if data.get("model_name"):
            domain.append(("model_name", "=", data["model_name"]))
        if data.get("user_id"):
            domain.append(("user_id", "=", data["user_id"]))

        AuditLog = self.env["facility.audit.log"]
        docs = AuditLog.search(domain, order="create_date desc") if domain else AuditLog.browse(docids)

        return {
            "doc_ids": docs.ids,
            "doc_model": "facility.audit.log",
            "docs": docs,
            "filters": data,
            "generated_on": fields.Datetime.now(),
            "generated_by": self.env.user.name,
        }


# =========================================================================
# Dashboard Aggregator
# =========================================================================
# =========================================================================
# Dashboard PDF Report Parser
# =========================================================================
class DashboardReportParser(models.AbstractModel):
    """Feeds report/dashboard_report.xml. Not tied to a specific record's
    data (the dashboard aggregates across the whole system), so `docids`
    is expected to just be the printing company's id - see the
    `action_server_print_dashboard_report` server action in
    views/report_views.xml for how this gets triggered."""

    _name = "report.facility_management.report_dashboard_document"
    _description = "Dashboard Report Parser"

    @api.model
    def _get_report_values(self, docids, data=None):
        dashboard_data = self.env["facility.report.dashboard"].get_dashboard_data()
        return {
            "doc_ids": docids,
            "doc_model": "res.company",
            "docs": self.env["res.company"].browse(docids),
            "dashboard": dashboard_data,
            "generated_on": fields.Datetime.now(),
            "generated_by": self.env.user.name,
        }


class FacilityReportDashboard(models.AbstractModel):
    """Non-persisted aggregator model. Not stored in DB - `get_dashboard_data`
    is called on demand (e.g. from a JS dashboard widget or
    report/dashboard_report.xml) and returns a plain dict of KPIs.

    Kept as an AbstractModel (rather than a regular model) since a
    dashboard has no records of its own; it only aggregates data that
    already lives on facility.asset / facility.booking / facility.maintenance
    / facility.audit.log.
    """

    _name = "facility.report.dashboard"
    _description = "Facility Management Dashboard"

    @api.model
    def get_dashboard_data(self, date_from=None, date_to=None):
        """Return a single dict with all KPIs the dashboard needs.

        :param date_from: optional str/date, lower bound for time-boxed KPIs
        :param date_to: optional str/date, upper bound for time-boxed KPIs
        """
        Asset = self.env["facility.asset"]
        Booking = self.env["facility.booking"]
        Maintenance = self.env["facility.maintenance"]
        AuditLog = self.env["facility.audit.log"]

        date_to = date_to or fields.Date.today()
        date_from = date_from or (date_to - timedelta(days=30))

        maintenance_domain = [("request_date", ">=", date_from), ("request_date", "<=", date_to)]
        maintenance_records = Maintenance.search(maintenance_domain)

        data = {
            "date_from": date_from,
            "date_to": date_to,

            # --- Asset KPIs ---
            "total_assets": Asset.search_count([]),

            # --- Booking KPIs ---
            "total_bookings": Booking.search_count([]),

            # --- Maintenance KPIs ---
            "maintenance_total": len(maintenance_records),
            "maintenance_open": len(
                maintenance_records.filtered(lambda r: r.state in ("draft", "confirmed", "in_progress"))
            ),
            "maintenance_overdue": len(maintenance_records.filtered("is_overdue")),
            "maintenance_completed": len(maintenance_records.filtered(lambda r: r.state == "done")),
            "maintenance_by_type": self._group_count(maintenance_records, "maintenance_type"),
            "maintenance_by_priority": self._group_count(maintenance_records, "priority"),
            "total_maintenance_cost": sum(maintenance_records.mapped("actual_cost")),

            # --- Audit KPIs ---
            "audit_events_total": AuditLog.search_count(
                [("create_date", ">=", date_from), ("create_date", "<=", date_to)]
            ),
            "audit_by_action": self._group_count(
                AuditLog.search([("create_date", ">=", date_from), ("create_date", "<=", date_to)]),
                "action_type",
            ),
        }
        return data

    @api.model
    def _group_count(self, records, field_name):
        """Small helper: {selection_value: count} for a Selection field on
        an in-memory recordset (kept simple/readable over a raw read_group
        since dashboard volumes are expected to be modest)."""
        result = {}
        for rec in records:
            key = rec[field_name] or "undefined"
            result[key] = result.get(key, 0) + 1
        return result