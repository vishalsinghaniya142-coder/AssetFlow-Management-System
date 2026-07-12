/** @odoo-module **/

document.addEventListener("DOMContentLoaded", function () {

    console.log("AssetFlow Maintenance Module Loaded");

    // =====================================
    // Maintenance Search
    // =====================================

    const maintenanceSearch = document.getElementById("maintenance_search");

    if (maintenanceSearch) {

        maintenanceSearch.addEventListener("keyup", function () {

            const value = this.value.toLowerCase();

            document.querySelectorAll("table tbody tr").forEach(function (row) {

                const text = row.innerText.toLowerCase();

                row.style.display = text.includes(value) ? "" : "none";

            });

        });

    }

    // =====================================
    // Maintenance Form Validation
    // =====================================

    const maintenanceForm = document.getElementById("maintenance_form");

    if (maintenanceForm) {

        maintenanceForm.addEventListener("submit", function (event) {

            const asset = document.getElementById("maintenance_asset");
            const date = document.getElementById("maintenance_date");

            if (
                !asset ||
                asset.value.trim() === "" ||
                !date ||
                date.value.trim() === ""
            ) {

                alert("Please complete all required fields.");

                event.preventDefault();

            }

        });

    }

    // =====================================
    // Status Counter
    // =====================================

    function updateMaintenanceCounter() {

        const pending =
            document.querySelectorAll(".maintenance-pending").length;

        const progress =
            document.querySelectorAll(".maintenance-progress").length;

        const completed =
            document.querySelectorAll(".maintenance-completed").length;

        if (document.getElementById("maintenance_pending"))
            document.getElementById("maintenance_pending").innerText = pending;

        if (document.getElementById("maintenance_progress"))
            document.getElementById("maintenance_progress").innerText = progress;

        if (document.getElementById("maintenance_completed"))
            document.getElementById("maintenance_completed").innerText = completed;

    }

    updateMaintenanceCounter();

    // =====================================
    // Delete Confirmation
    // =====================================

    document.querySelectorAll(".delete-maintenance").forEach(function (button) {

        button.addEventListener("click", function (event) {

            if (!confirm("Delete this maintenance record?")) {

                event.preventDefault();

            }

        });

    });

    // =====================================
    // Highlight Selected Row
    // =====================================

    document.querySelectorAll("table tbody tr").forEach(function (row) {

        row.addEventListener("click", function () {

            document
                .querySelectorAll("table tbody tr")
                .forEach(function (r) {
                    r.classList.remove("selected-row");
                });

            this.classList.add("selected-row");

        });

    });

});