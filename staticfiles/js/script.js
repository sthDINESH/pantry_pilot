document.addEventListener("DOMContentLoaded", function () {
  // Utility functions
  // Function to check if element hidden with bs collapse is visible
  function isElementShown(element) {
    return (
      element.classList.contains("show") ||
      element.classList.contains("collapsing") ||
      (!element.classList.contains("collapse") &&
        window.getComputedStyle(element).display !== "none")
    );
  }

  const deleteModal = new bootstrap.Modal(
    document.querySelector("#delete-modal")
  );
  const deleteModalBody = document.querySelector("#delete-modal .modal-body");
  const deleteConfirm = document.querySelector("#delete-confirm");

  // Auto show duplicate item modal for user input if it exists in DOM
  const duplicateItemModal = document.querySelector("#duplicate-item-modal");
  if (duplicateItemModal) {
    const modal = new bootstrap.Modal(duplicateItemModal);
    modal.show();

    // Listen for modal dismissal
    duplicateItemModal.addEventListener("hidden.bs.modal", function (event) {
      // Redirect to pantry when modal is completely hidden
      window.location.href =
        duplicateItemModal.getAttribute("data-redirect-url");
    });
  }

  // Event listeners
  const buttons = document.querySelectorAll("button");
  buttons.forEach((button) => {
    let buttonType = button.getAttribute("data-type");

    if (buttonType === "pantry-item-delete") {
      // Delete items from pantry
      button.addEventListener("click", function (event) {
        const pantryItemId = event.currentTarget.getAttribute("data-item-id");
        deleteModalBody.innerHTML = `
            <p>
            Are you sure you want to remove <strong>${button.getAttribute(
              "data-item-name"
            )}</strong> from pantry?
            <br>
            This action cannot be undone!
            </p>
        `;
        deleteConfirm.href = `item/${pantryItemId}/delete`;
        deleteModal.show();
      });
    } else if (buttonType === "category-delete") {
      // Delete entire category
      button.addEventListener("click", function (event) {
        const categoryId = event.currentTarget.getAttribute("data-category-id");
        deleteModalBody.innerHTML = `
            <p>
            Are you sure you want to remove <strong>${event.currentTarget.getAttribute(
              "data-category"
            )}</strong> from pantry?
            <br>
            All <em>${event.currentTarget.getAttribute(
              "data-category"
            )}</em> items will be removed and this action cannot be undone!
            </p>
        `;
        deleteConfirm.href = `category/${categoryId}/delete`;
        deleteModal.show();
      });
    } else if (buttonType === "pantry-item-update") {
      // Update items in pantry
      button.addEventListener("click", function (event) {
        const pantryItemForm = document.querySelector("#pantry-item-form");

        // Get the PK for pantry item and related category
        const itemId = event.currentTarget.getAttribute("data-item-id");
        const categoryId = event.currentTarget.getAttribute("data-category-id");

        // Copy the pantry item attributes to populate the form
        pantryItemForm.querySelector("#id_name").value = document.querySelector(
          `#item-${itemId} .pantry-item-name`
        ).innerText;
        pantryItemForm.querySelector("#id_quantity").value =
          document.querySelector(
            `#item-${itemId} .pantry-item-quantity`
          ).innerText;
        pantryItemForm.querySelector("#id_units").value = document
          .querySelector(`#item-${itemId} .pantry-item-units`)
          .getAttribute("data-item-units");
        pantryItemForm.querySelector("#id_category_name").value = document
          .querySelector(`#category-${categoryId} .sub-heading`)
          .getAttribute("data-category-name");

        // Add a button to cancel the update if not present
        let cancelButton = pantryItemForm.querySelector("#cancel-button");
        if (!cancelButton) {
          cancelButton = document.createElement("button");
          cancelButton.id = "cancel-button";
          cancelButton.innerText = "Cancel";
          cancelButton.classList.add("btn", "btn-danger");
          pantryItemForm.appendChild(cancelButton);
          cancelButton.addEventListener("click", function (event) {
            // Reset the pantry item form fields to defaults
            pantryItemForm.querySelector("#id_name").value = "";

            pantryItemForm.querySelector("#id_quantity").value = "";
            pantryItemForm.querySelector("#id_units").value = "piece";
            pantryItemForm.querySelector("#id_category_name").value = "other";

            // Change Update button back to add
            document.querySelector("#pantry-submit-button").innerText = "Add";
            // Update form action
            pantryItemForm.setAttribute("action", "");

            // Delete the cancel button
            document.querySelector("#cancel-button").remove();
          });
        }

        // Update the submit form button
        document.querySelector("#pantry-submit-button").innerText = "Update";
        // Update form action
        pantryItemForm.setAttribute("action", `item/${itemId}/update`);

        // Check if form is already visible before showing
        const formAlreadyVisible = isElementShown(pantryItemForm);

        if (!formAlreadyVisible) {
          // Show the form and scroll to it
          const bsCollapse =
            bootstrap.Collapse.getOrCreateInstance(pantryItemForm);
          bsCollapse.show();

          // Handle post-show actions
          pantryItemForm.addEventListener(
            "shown.bs.collapse",
            function onShown() {
              pantryItemForm.scrollIntoView({
                behavior: "smooth",
                block: "center",
              });

              setTimeout(() => {
                pantryItemForm.querySelector("#id_quantity").focus();
              }, 300);

              // Remove event listener after first use
              pantryItemForm.removeEventListener("shown.bs.collapse", onShown);
            }
          );
        } else {
          // Form is already visible, just scroll to it and focus
          pantryItemForm.scrollIntoView({
            behavior: "smooth",
            block: "center",
          });
          setTimeout(() => {
            pantryItemForm.querySelector("#id_quantity").focus();
          }, 300);
        }
      });
    }
  });

  gsap.from(".auth-grid-container .square-card", {
    y: 1000,
    duration: 1,
    stagger: 0.1,
  });
});
