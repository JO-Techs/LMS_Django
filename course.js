document.addEventListener("DOMContentLoaded", function () {
  // Form Validation
  const forms = document.querySelectorAll(".needs-validation");
  forms.forEach((form) => {
    form.addEventListener("submit", function (event) {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      }
      form.classList.add("was-validated");
    });
  });

  // Date Validation
  const startDateInput = document.querySelector('input[name="start_date"]');
  const endDateInput = document.querySelector('input[name="end_date"]');

  if (startDateInput && endDateInput) {
    // Set minimum date as today
    const today = new Date().toISOString().split("T")[0];
    startDateInput.setAttribute("min", today);

    // Update end date minimum when start date changes
    startDateInput.addEventListener("change", function () {
      endDateInput.setAttribute("min", this.value);
      if (endDateInput.value && endDateInput.value < this.value) {
        endDateInput.value = this.value;
      }
    });
  }

  // File Upload Preview
  const fileInputs = document.querySelectorAll('input[type="file"]');
  fileInputs.forEach((input) => {
    input.addEventListener("change", function () {
      const file = this.files[0];
      if (file) {
        const fileSize = (file.size / 1024 / 1024).toFixed(2); // Convert to MB
        const fileType = file.type;
        const allowedTypes = [
          "application/pdf",
          "image/jpeg",
          "image/png",
          "application/msword",
          "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ];

        // Validate file type and size
        if (!allowedTypes.includes(fileType)) {
          alert(
            "Invalid file type. Please upload PDF, JPEG, PNG, or DOC files."
          );
          this.value = "";
          return;
        }

        if (fileSize > 5) {
          alert("File size must be less than 5MB");
          this.value = "";
          return;
        }

        // Create preview
        const previewContainer =
          this.parentElement.querySelector(".file-preview") ||
          document.createElement("div");
        previewContainer.className = "file-preview";
        previewContainer.innerHTML = `
                    <div class="alert alert-info">
                        <strong>Selected File:</strong> ${file.name}<br>
                        <strong>Size:</strong> ${fileSize}MB<br>
                        <strong>Type:</strong> ${fileType}
                    </div>
                `;

        if (!this.parentElement.querySelector(".file-preview")) {
          this.parentElement.appendChild(previewContainer);
        }
      }
    });
  });

  // Course Module Management
  const moduleList = document.getElementById("moduleList");
  if (moduleList) {
    // Initialize Sortable for drag-and-drop functionality
    new Sortable(moduleList, {
      animation: 150,
      handle: ".module-handle",
      onEnd: function (evt) {
        updateModuleOrder();
      },
    });

    // Update module order after drag and drop
    function updateModuleOrder() {
      const modules = Array.from(moduleList.children).map((el, index) => ({
        id: el.dataset.moduleId,
        order: index + 1,
      }));

      // Send AJAX request to update order
      fetch("/update-module-order/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
            .value,
        },
        body: JSON.stringify({ modules: modules }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            // Update order numbers in UI
            modules.forEach((module) => {
              const moduleEl = document.querySelector(
                `[data-module-id="${module.id}"]`
              );
              const orderBadge = moduleEl.querySelector(".module-order");
              if (orderBadge) {
                orderBadge.textContent = `Module ${module.order}`;
              }
            });
          }
        })
        .catch((error) => console.error("Error updating module order:", error));
    }
  }

  // Dynamic Form Fields
  const addFieldButton = document.querySelector(".add-field-button");
  if (addFieldButton) {
    addFieldButton.addEventListener("click", function () {
      const fieldContainer = document.querySelector(".dynamic-fields");
      const fieldCount = fieldContainer.children.length;

      const newField = document.createElement("div");
      newField.className = "mb-3 dynamic-field";
      newField.innerHTML = `
                <div class="input-group">
                    <input type="text" name="field_${fieldCount}" class="form-control" placeholder="Enter field content">
                    <button type="button" class="btn btn-danger remove-field">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            `;

      fieldContainer.appendChild(newField);
    });

    // Remove dynamic field
    document.addEventListener("click", function (e) {
      if (e.target.classList.contains("remove-field")) {
        e.target.closest(".dynamic-field").remove();
      }
    });
  }

  // Course Search/Filter
  const searchInput = document.querySelector(".course-search");
  if (searchInput) {
    searchInput.addEventListener(
      "input",
      debounce(function () {
        const searchTerm = this.value.toLowerCase();
        const courseCards = document.querySelectorAll(".course-card");

        courseCards.forEach((card) => {
          const title = card
            .querySelector(".course-title")
            .textContent.toLowerCase();
          const description = card
            .querySelector(".course-description")
            .textContent.toLowerCase();

          if (title.includes(searchTerm) || description.includes(searchTerm)) {
            card.style.display = "";
          } else {
            card.style.display = "none";
          }
        });
      }, 300)
    );
  }

  // Debounce function for search
  function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  // Confirmation Dialogs
  const confirmActions = document.querySelectorAll("[data-confirm]");
  confirmActions.forEach((element) => {
    element.addEventListener("click", function (e) {
      if (!confirm(this.dataset.confirm)) {
        e.preventDefault();
      }
    });
  });
});
