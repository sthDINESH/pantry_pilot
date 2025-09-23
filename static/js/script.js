document.addEventListener("DOMContentLoaded", function () {
  console.log("DEBUG: Hello world!");

  const deleteModal = new bootstrap.Modal(
    document.querySelector("#delete-modal")
  );
  const deleteModalBody = document.querySelector("#delete-modal .modal-body");
  const deleteConfirm = document.querySelector("#delete-confirm");

  //   Add event listeners
  const buttons = document.querySelectorAll("button");
  buttons.forEach((button) => {
    let buttonType = button.getAttribute("data-type");
    if (buttonType === "pantry-item-delete") {
      button.addEventListener("click", function (event) {
        const pantryItemId = event.target.getAttribute("data-item-id");
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
      button.addEventListener("click", function (event) {
        const categoryId = event.target.getAttribute("data-category-id");
        deleteModalBody.innerHTML = `
            <p>
            Are you sure you want to remove <strong>${event.target.getAttribute(
              "data-category"
            )}</strong> from pantry?
            <br>
            All <em>${event.target.getAttribute(
              "data-category"
            )}</em> items will be removed and this action cannot be undone!
            </p>
        `;
        deleteConfirm.href = `category/${categoryId}/delete`;
        deleteModal.show();
      });
    } else if (buttonType === "pantry-item-update") {
      button.addEventListener("click", function (event) {
        const pantryItemForm = document.querySelector("#pantry-item-form");
        // Get the PK for pantry item and related category
        const itemId = event.target.getAttribute("data-item-id");
        const categoryId = event.target.getAttribute("data-category-id");

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

        // Update the submit form button
        document.querySelector("#pantry-submit-button").innerText = "Update";
        // Update form action
        pantryItemForm.setAttribute("action", `item/${itemId}/update`);

        // Add a button to cancel the update
        const cancelButton = document.createElement("button");
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
      });
    }
  });

  gsap.from(".auth-grid-container .square-card", {
    y: 1000,
    duration: 1,
    stagger: 0.1,
  });
});
