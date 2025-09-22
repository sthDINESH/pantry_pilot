document.addEventListener("DOMContentLoaded", function () {
  console.log("DEBUG: Hello world!");

  const deleteModal = new bootstrap.Modal(document.querySelector("#delete-modal"));
  const deleteModalBody = document.querySelector("#delete-modal .modal-body");
  const deleteConfirm = document.querySelector("#delete-confirm");

  //   Add event listeners
  const buttons = document.querySelectorAll("button");
  buttons.forEach((button) => {
    if (button.getAttribute("data-type") === "pantry-item-delete") {
      button.addEventListener("click", function (event) {
        const pantry_item_id = event.target.getAttribute("data-item-id");
        console.log(`DEBUG: Delete item id: ${pantry_item_id}`);
        deleteModalBody.innerHTML = `
            <p>
            Are you sure you want to remove <strong>${button.getAttribute("data-item-name")}</strong> from pantry?
            <br>
            This action cannot be undone!
            </p>
        `;
        deleteConfirm.href = `${pantry_item_id}/delete`;
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
