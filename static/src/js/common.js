/** @odoo-module **/

document.addEventListener("DOMContentLoaded", function () {

    console.log("AssetFlow Loaded Successfully");

    // -------------------------
    // Button Ripple Effect
    // -------------------------

    document.querySelectorAll("button").forEach((button) => {

        button.addEventListener("click", function () {

            this.style.opacity = "0.8";

            setTimeout(() => {

                this.style.opacity = "1";

            }, 200);

        });

    });

    // -------------------------
    // Table Row Hover
    // -------------------------

    document.querySelectorAll("table tbody tr").forEach((row) => {

        row.addEventListener("mouseenter", function () {

            this.style.transition = "0.2s";

        });

    });

    // -------------------------
    // Auto Hide Alerts
    // -------------------------

    document.querySelectorAll(".alert").forEach((alert) => {

        setTimeout(() => {

            alert.style.display = "none";

        }, 3000);

    });

});