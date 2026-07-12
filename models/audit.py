# -*- coding: utf-8 -*-
"""
Audit Module
------------
Provides a centralized, immutable audit trail for the facility management
system, plus a reusable mixin (`facility.audit.mixin`) that other models
(asset, booking, maintenance, etc.) can inherit to get automatic
create/write/unlink logging without duplicating code.

Author : Member 4 (Maintenance, Audit, Reports & Security)
Module : facility_management
"""

import json
import logging

from odoo import api, fields, models, _
from odoo.exceptions import AccessError

_logger = logging.getLogger(__name__)


class FacilityAuditLog(models.Model):
    """Immutable audit trail entry.

    Every row represents a single tracked event (create / write / unlink /
    state change / security event) on any model in the system. Records are
    write-once: update and delete are blocked at the ORM level so the trail
    cannot be tampered with, except by a technical/admin user via SQL
    (which is, itself, the intended safeguard for an audit log).
    """

    _name = "facility.audit.log"
    _description = "Facility Audit Log"
    _order = "create_date desc, id desc"
    _rec_name = "display_name"

    # ------------------------------------------------------------------
    # What happened
    # ------------------------------------------------------------------
    action_type = fields.Selection(
        selection=[
            ("create", "Create"),
            ("write", "Update"),
            ("unlink", "Delete"),
            ("state_change", "Status Change"),
            ("login", "Login"),
            ("logout", "Logout"),
            ("access_denied", "Access Denied"),
            ("other", "Other"),
        ],
        string="Action",
        required=True,
        index=True,
    )

    description = fields.Char(
        string="Summary",
        help="Short, human-readable description of what happened.",
    )

    # ------------------------------------------------------------------
    # On what record
    # ------------------------------------------------------------------
    model_name = fields.Char(string="Model", required=True, index=True)
    res_id = fields.Integer(string="Record ID", index=True)
    record_name = fields.Char(
        string="Record Reference",
        help="Snapshot of the record's display name at the time of logging "
             "(kept even if the record is later deleted).",
    )

    display_name = fields.Char(compute="_compute_display_name", store=False)

    # ------------------------------------------------------------------
    # Change detail (for write actions)
    # ------------------------------------------------------------------
    old_values = fields.Text(string="Old Values (JSON)")
    new_values = fields.Text(string="New Values (JSON)")

    # ------------------------------------------------------------------
    # Who / when / from where
    # ------------------------------------------------------------------
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User",
        required=True,
        default=lambda self: self.env.user,
        index=True,
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.company,
    )
    ip_address = fields.Char(string="IP Address")
    create_date = fields.Datetime(string="Logged At", readonly=True)

    # ------------------------------------------------------------------
    # Compute
    # ------------------------------------------------------------------
    @api.depends("action_type", "model_name", "record_name")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = "[%s] %s - %s" % (
                dict(rec._fields["action_type"].selection).get(rec.action_type, ""),
                rec.model_name or "",
                rec.record_name or rec.res_id or "",
            )

    # ------------------------------------------------------------------
    # Immutability guard
    # ------------------------------------------------------------------
    def write(self, vals):
        raise AccessError(_("Audit log entries are immutable and cannot be edited."))

    def unlink(self):
        raise AccessError(
            _("Audit log entries cannot be deleted. Use the archival/cleanup "
              "cron job instead if retention policy requires purging.")
        )

    # ------------------------------------------------------------------
    # Helper API used by the mixin (and can be called directly elsewhere,
    # e.g. security.py for login/logout or access-denied events)
    # ------------------------------------------------------------------
    @api.model
    def log_action(self, model_name, res_id, action_type, description=None,
                    record_name=None, old_values=None, new_values=None):
        """Create a single audit log entry.

        Uses sudo() so that logging never fails (or gets blocked) due to the
        acting user's own access rights on the audit log model.
        """
        request_ip = None
        try:
            from odoo.http import request
            if request:
                request_ip = request.httprequest.remote_addr
        except Exception:  # pragma: no cover - request not always available
            request_ip = None

        vals = {
            "action_type": action_type,
            "model_name": model_name,
            "res_id": res_id or 0,
            "record_name": record_name,
            "description": description,
            "old_values": json.dumps(old_values, default=str) if old_values else False,
            "new_values": json.dumps(new_values, default=str) if new_values else False,
            "user_id": self.env.uid,
            "ip_address": request_ip,
        }
        return self.sudo().create(vals)

    @api.model
    def purge_old_logs(self, retention_days=365):
        """Intended to be called from a scheduled cron job
        (see data/cron_jobs.xml) to purge logs older than the retention
        period. Uses raw SQL since normal unlink() is blocked above.
        """
        query = """
            DELETE FROM facility_audit_log
            WHERE create_date < (NOW() - INTERVAL %s)
        """
        self.env.cr.execute(query, (f"{retention_days} days",))
        _logger.info(
            "Audit log purge executed: removed entries older than %s days.",
            retention_days,
        )


class FacilityAuditMixin(models.AbstractModel):
    """Abstract mixin. Inherit this in any model (e.g. facility.asset,
    facility.booking, facility.maintenance) to get automatic audit logging
    of create / write / unlink actions with zero extra code:

        class FacilityAsset(models.Model):
            _name = "facility.asset"
            _inherit = ["facility.audit.mixin", "mail.thread"]
            ...

    Fields listed in `_audit_track_fields` (override per-model) are the
    only ones captured in the old/new value diff on write(); leave empty
    to track all stored fields.
    """

    _name = "facility.audit.mixin"
    _description = "Facility Audit Mixin"

    # Override in the inheriting model to limit which fields are diffed.
    # Empty list = track all stored, non-relational-heavy fields.
    _audit_track_fields = []

    def _get_audit_trackable_fields(self):
        self.ensure_one()
        if self._audit_track_fields:
            return self._audit_track_fields
        return [
            fname
            for fname, field in self._fields.items()
            if field.store and not field.compute and fname not in ("write_date", "write_uid")
        ]

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        AuditLog = self.env["facility.audit.log"]
        for record in records:
            AuditLog.log_action(
                model_name=record._name,
                res_id=record.id,
                action_type="create",
                description=_("%s created.") % record._description,
                record_name=record.display_name if hasattr(record, "display_name") else str(record.id),
                new_values={f: record[f] for f in record._get_audit_trackable_fields() if f in record},
            )
        return records

    def write(self, vals):
        AuditLog = self.env["facility.audit.log"]
        old_snapshot = {
            rec.id: {f: rec[f] for f in vals.keys() if f in rec._fields}
            for rec in self
        }
        result = super().write(vals)
        for record in self:
            AuditLog.log_action(
                model_name=record._name,
                res_id=record.id,
                action_type="write",
                description=_("%s updated.") % record._description,
                record_name=record.display_name if hasattr(record, "display_name") else str(record.id),
                old_values=old_snapshot.get(record.id),
                new_values={f: record[f] for f in vals.keys() if f in record._fields},
            )
        return result

    def unlink(self):
        AuditLog = self.env["facility.audit.log"]
        snapshot = [
            {
                "id": rec.id,
                "name": rec.display_name if hasattr(rec, "display_name") else str(rec.id),
                "model": rec._name,
                "description": rec._description,
            }
            for rec in self
        ]
        result = super().unlink()
        for item in snapshot:
            AuditLog.log_action(
                model_name=item["model"],
                res_id=item["id"],
                action_type="unlink",
                description=_("%s deleted.") % item["description"],
                record_name=item["name"],
            )
        return result