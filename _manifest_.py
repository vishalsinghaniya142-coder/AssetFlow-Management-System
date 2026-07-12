# -*- coding: utf-8 -*-

{
    "name": "AssetFlow Management System",
    "version": "17.0.1.0.0",
    "summary": "Smart Asset Management System",
    "description": """
AssetFlow Management System

Features:
- Asset Management
- Employee Management
- Dashboard
- Booking
- Maintenance
- Reports
- Notifications
- Settings
- REST API
""",

    "author": "Hackathon Team",
    "website": "",
    "category": "Inventory",
    "license": "LGPL-3",

    "depends": [
        "base",
        "mail",
        "web",
    ],

    "data": [

        # Security
        "security/security.xml",
        "security/asset_security.xml",
        "security/booking_security.xml",
        "security/maintenance_security.xml",
        "security/ir.model.access.csv",

        # Data
        "data/asset_sequence.xml",
        "data/department_data.xml",
        "data/employee_data.xml",
        "data/category_data.xml",
        "data/notification_data.xml",
        "data/cron_jobs.xml",
        "data/mail_templates.xml",

        # Views
        "views/menu.xml",
        "views/dashboard_views.xml",
        "views/employee_views.xml",
        "views/department_views.xml",
        "views/asset_category_views.xml",
        "views/asset_views.xml",
        "views/asset_allocation_views.xml",
        "views/asset_transfer_views.xml",
        "views/booking_views.xml",
        "views/maintenance_views.xml",
        "views/audit_views.xml",
        "views/report_views.xml",
        "views/notification_views.xml",
        "views/search_views.xml",
        "views/settings_views.xml",

        # Wizards
        "wizard/allocate_asset_views.xml",
        "wizard/return_asset_views.xml",
        "wizard/booking_wizard_views.xml",
        "wizard/maintenance_wizard_views.xml",

        # Reports
        "report/asset_report.xml",
        "report/booking_report.xml",
        "report/maintenance_report.xml",
        "report/audit_report.xml",
        "report/dashboard_report.xml",
        "report/report_templates.xml",
    ],

    "demo": [
        "demo/demo.xml",
        "demo/asset_demo.xml",
        "demo/employee_demo.xml",
    ],

    "assets": {
        "web.assets_backend": [

            # CSS
            "AssetFlow-Management-System/static/src/css/common.css",
            "AssetFlow-Management-System/static/src/css/dashboard.css",
            "AssetFlow-Management-System/static/src/css/assets.css",
            "AssetFlow-Management-System/static/src/css/booking.css",
            "AssetFlow-Management-System/static/src/css/maintenance.css",
            "AssetFlow-Management-System/static/src/css/reports.css",

            # JavaScript
            "AssetFlow-Management-System/static/src/js/common.js",
            "AssetFlow-Management-System/static/src/js/dashboard.js",
            "AssetFlow-Management-System/static/src/js/assets.js",
            "AssetFlow-Management-System/static/src/js/booking.js",
            "AssetFlow-Management-System/static/src/js/maintenance.js",
            "AssetFlow-Management-System/static/src/js/reports.js",

            # QWeb Templates
            "AssetFlow-Management-System/static/src/xml/dashboard_templates.xml",
        ],
    },

    "images": [
        "static/src/img/logo.png",
    ],

    "installable": True,
    "application": True,
    "auto_install": False,
}