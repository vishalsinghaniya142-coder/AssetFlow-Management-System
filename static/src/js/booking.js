/** @odoo-module **/

document.addEventListener("DOMContentLoaded", function () {

    console.log("AssetFlow Booking Module Loaded");

    // =====================================
    // Booking Search
    // =====================================

    const bookingSearch = document.getElementById("booking_search");

    if (bookingSearch) {

        bookingSearch.addEventListener("keyup", function () {

            const value = this.value.toLowerCase();

            document.querySelectorAll("table tbody tr").forEach(function (row) {

                const text = row.innerText.toLowerCase();

                row.style.display = text.includes(value) ? "" : "none";

            });

        });

    }

    // =====================================
    // Booking Form Validation
    // =====================================

    const bookingForm = document.getElementById("booking_form");

    if (bookingForm) {

        bookingForm.addEventListener("submit", function (event) {

            const employee = document.getElementById("employee_name");
            const asset = document.getElementById("asset_name");

            if (
                !employee ||
                employee.value.trim() === "" ||
                !asset ||
                asset.value.trim() === ""
            ) {

                alert("Employee and Asset are required.");

                event.preventDefault();

            }

        });

    }

    // =====================================
    // Booking Status Counter
    // =====================================

    function updateBookingCounter() {

        const pending =
            document.querySelectorAll(".status-pending").length;

        const approved =
            document.querySelectorAll(".status-approved").length;

        const cancelled =
            document.querySelectorAll(".status-cancelled").length;

        if (document.getElementById("pending_booking"))
            document.getElementById("pending_booking").innerText = pending;

        if (document.getElementById("approved_booking"))
            document.getElementById("approved_booking").innerText = approved;

        if (document.getElementById("cancelled_booking"))
            document.getElementById("cancelled_booking").innerText = cancelled;

    }

    updateBookingCounter();

    // =====================================
    // Delete Confirmation
    // =====================================

    document.querySelectorAll(".delete-booking").forEach(function (button) {

        button.addEventListener("click", function (event) {

            if (!confirm("Delete this booking?")) {

                event.preventDefault();

            }

        });

    });

});