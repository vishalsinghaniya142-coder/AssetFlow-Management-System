/** @odoo-module **/

document.addEventListener("DOMContentLoaded", function () {

    console.log("AssetFlow Assets Loaded");

    // ======================================
    // Asset Search
    // ======================================

    const searchBox = document.getElementById("asset_search");

    if (searchBox) {

        searchBox.addEventListener("keyup", function () {

            let value = this.value.toLowerCase();

            document.querySelectorAll("table tbody tr").forEach(function (row) {

                let text = row.innerText.toLowerCase();

                if (text.indexOf(value) > -1) {
                    row.style.display = "";
                } else {
                    row.style.display = "none";
                }

            });

        });

    }

    // ======================================
    // Delete Confirmation
    // ======================================

    document.querySelectorAll(".delete-asset").forEach(function (button) {

        button.addEventListener("click", function (event) {

            let confirmDelete = confirm(
                "Are you sure you want to delete this asset?"
            );

            if (!confirmDelete) {
                event.preventDefault();
            }

        });

    });

    // ======================================
    // Highlight Selected Row
    // ======================================

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

    // ======================================
    // Status Counter
    // ======================================

    function updateStatusCounter() {

        let available = document.querySelectorAll(".available").length;
        let assigned = document.querySelectorAll(".assigned").length;
        let maintenance = document.querySelectorAll(".maintenance").length;
        let retired = document.querySelectorAll(".retired").length;

        if (document.getElementById("available_count"))
            document.getElementById("available_count").innerText = available;

        if (document.getElementById("assigned_count"))
            document.getElementById("assigned_count").innerText = assigned;

        if (document.getElementById("maintenance_count"))
            document.getElementById("maintenance_count").innerText = maintenance;

        if (document.getElementById("retired_count"))
            document.getElementById("retired_count").innerText = retired;

    }

    updateStatusCounter();

});