// Handle alert dismissal
document.addEventListener("DOMContentLoaded", function () {
  // Auto dismiss alerts after 5 seconds
  setTimeout(function () {
    const alerts = document.querySelectorAll(".alert");
    alerts.forEach((alert) => {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    });
  }, 5000);

  // Form validation
  const forms = document.querySelectorAll(".needs-validation");
  forms.forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      }
      form.classList.add("was-validated");
    });
  });

  // Confirm actions
  const confirmActions = document.querySelectorAll("[data-confirm]");
  confirmActions.forEach((element) => {
    element.addEventListener("click", (event) => {
      if (!confirm(element.dataset.confirm)) {
        event.preventDefault();
      }
    });
  });
});
