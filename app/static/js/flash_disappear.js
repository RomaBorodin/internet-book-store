document.addEventListener("DOMContentLoaded", function () {
        const alerts = document.querySelectorAll(".alert");

        alerts.forEach(alert => {
            setTimeout(() => {
                let bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 2000);
        });
    });