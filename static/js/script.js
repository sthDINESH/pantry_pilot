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
    if (button.getAttribute("data-type") === "pantry-item-delete") {
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
    } else if (button.getAttribute("data-type") === "category-delete") {
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
    }
  });

  gsap.from(".auth-grid-container .square-card", {
    y: 1000,
    duration: 1,
    stagger: 0.1,
  });
});
