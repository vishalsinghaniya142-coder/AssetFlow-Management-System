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
        "security/security.xml",
        "security/asset_security.xml",
        "security/booking_security.xml",
        "security/maintenance_security.xml",
        "security/ir.model.access.csv",

        "data/asset__sequence.xml",
        "data/department_data.xml",
        "data/employee_data.xml",
        "data/category_data.xml",
        "data/notification_data.xml",
        "data/cron_jobs.xml",
        "data/mail_templates.xml",

        "views/menu.xml",
        "views/dashboard_views.xml",
        "views/employee_view.xml",
        "views/department_view.xml",
        "views/asset_category_view.xml",
        "views/asset_view.xml",
        "views/asset_allocation_views.xml",
        "views/asset_transfer_views.xml",
        "views/booking_views.xml",
        "views/maintenance_views.xml",
        "views/audit_views.xml",
        "views/report_views.xml",
        "views/notification_views.xml",
        "views/search_views.xml",
        "views/setings_views.xml",

        "wizard/allocate_asset_views.xml",
        "wizard/return_assets_view.xml",
        "wizard/booking_wizards_views.xml",
        "wizard/maintenance_wizard_views.xml",

        "reports/assest_report.xml",
        "reports/booking_report.xml",
        "reports/maintenance_report.xml",
        "reports/audit_report.xml",
        "reports/dashboard_report.xml",
        "reports/report_templates.xml",
    ],

    "demo": [
        "demo/demo.xml",
    ],

    "assets": {
        "web.assets_backend": [
            "AssetFlow-Management-System/static/src/css/common.css",
            "AssetFlow-Management-System/static/src/css/dashboard.css",
            "AssetFlow-Management-System/static/src/css/assets.css",
            "AssetFlow-Management-System/static/src/css/booking.css",
            "AssetFlow-Management-System/static/src/css/maintenance.css",
            "AssetFlow-Management-System/static/src/css/report.css",

            "AssetFlow-Management-System/static/src/js/common.js",
            "AssetFlow-Management-System/static/src/js/dasboard.js",
            "AssetFlow-Management-System/static/src/js/assets.js",
            "AssetFlow-Management-System/static/src/js/booking.js",
            "AssetFlow-Management-System/static/src/js/maintenance.js",
            "AssetFlow-Management-System/static/src/js/report.js",
        ],
    },

    "images": [
        "static/src/img/logo.png",
    ],

    "installable": True,
    "application": True,
    "auto_install": False,
}
