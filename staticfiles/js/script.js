document.addEventListener("DOMContentLoaded", function () {
  console.log("DEBUG: Hello world!");

  //   Add event listeners
  const buttons = document.querySelectorAll("button");
  buttons.forEach((button) => {
    if (button.getAttribute("data-type") === "pantry-item-delete") {
      button.addEventListener("click", function (event) {
        const pantry_item_id = event.target.getAttribute("data-item-id");
        console.log(`This will delete item id: ${pantry_item_id}`);
      });
    }
  });

  gsap.from(".auth-grid-container .square-card", {
    y: 1000,
    duration: 1,
    stagger: 0.1,
  });
});
