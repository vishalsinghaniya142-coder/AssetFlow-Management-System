{
    "name": "AssetFlow Management System",
    "version": "17.0.1.0.0",
    "summary": "Smart Asset Management System",
    "description": """
AssetFlow Management System

Main Features
-------------
* Dashboard
* Asset Management
* Settings
* REST API
* Portal
* Reports
* Testing Support
    """,

    "category": "Inventory",
    "author": "Hackathon Team",
    "website": "",
    "license": "LGPL-3",

    "depends": [
        "base",
        "mail",
        "web",
    ],

    "data": [
        "security/ir.model.access.csv",

        "views/menu.xml",
        "views/dashboard_views.xml",
        "views/settings_views.xml",
    ],

    "demo": [],

    "assets": {
        "web.assets_backend": [
            # Example
            # "assetflow_management_system/static/src/css/dashboard.css",
            # "assetflow_management_system/static/src/js/dashboard.js",
        ],
    },

    "images": [
        "static/description/icon.png",
    ],

    "installable": True,
    "application": True,
    "auto_install": False,
}