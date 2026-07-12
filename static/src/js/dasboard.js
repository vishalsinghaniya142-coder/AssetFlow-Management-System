/** @odoo-module **/

document.addEventListener("DOMContentLoaded", function () {

    console.log("AssetFlow Dashboard Loaded");

    // ==========================
    // Dashboard Counter Animation
    // ==========================

    function animateCounter(id) {

        const element = document.getElementById(id);

        if (!element) return;

        let target = parseInt(element.innerText) || 0;

        let count = 0;

        let speed = Math.max(5, Math.floor(target / 50));

        let interval = setInterval(function () {

            count += speed;

            if (count >= target) {

                count = target;

                clearInterval(interval);

            }

            element.innerText = count;

        }, 20);

    }

    animateCounter("total_assets");
    animateCounter("available_assets");
    animateCounter("assigned_assets");
    animateCounter("maintenance_assets");
    animateCounter("retired_assets");

    // ==========================
    // Refresh Button
    // ==========================

    const refreshBtn = document.getElementById("refresh_dashboard");

    if (refreshBtn) {

        refreshBtn.addEventListener("click", function () {

            location.reload();

        });

    }

    // ==========================
    // Dashboard Cards Hover
    // ==========================

    document.querySelectorAll(".dashboard-card").forEach(function(card){

        card.addEventListener("mouseenter", function(){

            this.style.transform = "translateY(-5px)";
            this.style.transition = ".3s";

        });

        card.addEventListener("mouseleave", function(){

            this.style.transform = "translateY(0px)";

        });

    });

});