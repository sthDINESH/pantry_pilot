document.addEventListener("DOMContentLoaded", function () {
  // Utility functions
  // ---------------------------------------------------------------
  // Function to check if element hidden with bs collapse is visible
  function isElementShown(element) {
    return (
      element.classList.contains("show") ||
      element.classList.contains("collapsing") ||
      (!element.classList.contains("collapse") &&
        window.getComputedStyle(element).display !== "none")
    );
  }

  // Handle collapse icon changes
  function updateCollapseIcon(button, state) {
    const icon = button.querySelector("i");
    if (!icon) return;

    const targetSelector = button.getAttribute("data-bs-target");

    if (targetSelector === "#pantry-item-form") {
      // Form collapse button (plus/minus)
      if (state === "expanded") {
        icon.className = "fa-solid fa-chevron-up";
      } else {
        icon.className = "fa-solid fa-plus";
      }
    } else if (targetSelector && targetSelector.startsWith("#category-body-")) {
      // Category collapse button (chevron up/down)
      if (state === "expanded") {
        icon.className = "fa-solid fa-chevron-up";
      } else {
        icon.className = "fa-solid fa-chevron-down";
      }
    }
  }

  // Parse search results JSON from DOM if available
  const searchResultsNode = document.querySelector("#search-data");
  let searchResults = {};
  if (searchResultsNode) {
    try {
      searchResults = JSON.parse(searchResultsNode.textContent);
    } catch (e) {
      console.error("Error parsing search results:", e);
    }
  }

  // ---------------------------------------------------------------
  // Create a BS modal object for base Modal if present
  const baseModalNode = document.querySelector("#base-modal");
  let baseModal = null;
  if (baseModalNode) {
    baseModal = new bootstrap.Modal(baseModalNode);
  }
  const baseModalBody = document.querySelector("#base-modal .modal-body");

  // Button with id delete-confirm in  Base modal
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
  // ---------------------------------------------------------------
  // Event listeners for button clicks
  const buttons = document.querySelectorAll("button");
  buttons.forEach((button) => {
    let buttonType = button.getAttribute("data-type");

    if (buttonType === "pantry-item-delete") {
      // Delete items from pantry
      button.addEventListener("click", function (event) {
        const pantryItemId = event.currentTarget.getAttribute("data-item-id");
        baseModalBody.innerHTML = `
            <p>
            Are you sure you want to remove <strong>${button.getAttribute(
              "data-item-name"
            )}</strong> from pantry?
            <br>
            This action cannot be undone!
            </p>
        `;
        deleteConfirm.href = `item/${pantryItemId}/delete`;
        baseModal.show();
      });
    } else if (buttonType === "category-delete") {
      // Delete entire category
      button.addEventListener("click", function (event) {
        const categoryId = event.currentTarget.getAttribute("data-category-id");
        baseModalBody.innerHTML = `
            <p>
            Are you sure you want to remove category <strong>${event.currentTarget.getAttribute(
              "data-category"
            )}</strong> from pantry?
            <br>
            All items in <em>${event.currentTarget.getAttribute(
              "data-category"
            )}</em> will be removed and this action cannot be undone!
            </p>
        `;
        deleteConfirm.href = `category/${categoryId}/delete`;
        baseModal.show();
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
          cancelButton.classList.add("btn", "btn-secondary", "form-button");
          pantryItemForm
            .querySelector(".form-button-controls")
            .appendChild(cancelButton);
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
    } else if (buttonType === "ingredients-count-info") {
      button.addEventListener("click", function (event) {
        // Display matched and missing ingredients for the recipe
        // Populate base modal with data
        const recipeId = event.currentTarget.getAttribute("data-recipe-id");
        const recipe = searchResults.find((recipe) => recipe.id == recipeId);

        if (!recipe) {
          baseModalBody.innerHTML = "<p>Recipe data not available.</p>";
          baseModal.show();
          return;
        }
        // Build modal content with full recipe data
        let modalContent = `
            <div class="recipe-modal-header container-fluid">
                <div class="row">
                  <div class="col-md-5">
                    <img src="${recipe.image}" alt="${recipe.title}">
                  </div>
                  <div class="col-md-7 d-flex align-items-center">
                    <h3>${recipe.title}</h3>
                  </div>
                </div>
            </div>
        `;

        if (
          recipe.used_ingredient_names &&
          recipe.used_ingredient_names.length > 0
        ) {
          modalContent += `
            <div class="container-fluid">
              <div class="ingredients-section row">
                <div class="col-12 category-section-heading">
                      In Your Pantry <span>(${recipe.used_ingredient_names.length} items)</span>
                </div>
                <div class="col-12"> 
                  <div class="row">
            `;
          recipe.used_ingredient_names.forEach((ingredient) => {
            modalContent += `
                    <div class="col-md-6">
                        <span class="mb-1">✓ ${ingredient}</span>
                    </div>
                `;
          });
          modalContent += `
                  </div>
                </div>
              </div>
            </div>
          `;
        }

        if (
          recipe.missed_ingredient_names &&
          recipe.missed_ingredient_names.length > 0
        ) {
          modalContent += `
            <div class="container-fluid">
              <div class="ingredients-section row">
                <div class="col-12 category-section-heading">
                  Need to Buy <span>(${recipe.missed_ingredient_names.length} items)</span>
                </div>
                <div class="col-12"> 
                  <div class="row">
            `;
          recipe.missed_ingredient_names.forEach((ingredient) => {
            modalContent += `
                    <div class="col-md-6">
                        <span class="mb-1">• ${ingredient}</span>
                    </div>
                `;
          });
        }

        // Update modal
        baseModalBody.innerHTML = modalContent;
        baseModal.show();
      });
    }
  });

  // Event listeners for collapse icon
  const collapseButtons = document.querySelectorAll(
    '[data-bs-toggle="collapse"]'
  );
  collapseButtons.forEach((button) => {
    const targetSelector = button.getAttribute("data-bs-target");
    const targetElement = document.querySelector(targetSelector);

    if (targetElement) {
      // Set initial state based on current classes
      const isExpanded = targetElement.classList.contains("show");
      updateCollapseIcon(button, isExpanded ? "expanded" : "collapsed");

      // Listen for Bootstrap collapse events
      targetElement.addEventListener("show.bs.collapse", function () {
        updateCollapseIcon(button, "expanded");
      });

      targetElement.addEventListener("hide.bs.collapse", function () {
        updateCollapseIcon(button, "collapsed");
      });
    }
  });

  // GSAP for animations
  // Register ScrollTrigger plugin
  // gsap.registerPlugin(ScrollTrigger);

  // // Scroll trigger animation for pantry item category images
  // console.log(document.querySelector("#pantry-section"));

  // // Create an object to animate
  // let imageSequence = { frame: 0 };

  // gsap.timeline(
  //   {
  //     onUpdate: updateCount,
  //     ScrollTrigger: {
  //       trigger: document.querySelector("#pantry-section"),
  //       start: "top 5%",
  //       end: "bottom 95%",
  //       scrub:1,
  //       pin:false,
  //       markers:true,
  //       onUpdate: self => {
  //         console.log("Progress:",self.progress);
  //       }
  //     }
  //   }
  // ).to(
  //   imageSequence,
  //   {
  //     frame: 5,
  //     ease: "none",
  //     duration: 1
  //   }
  // );

  // function updateCount (){
  //   console.log(Math.round(imageSequence.frame));
  // }

  // gsap.from(".auth-grid-container .square-card", {
  //   y: 1000,
  //   duration: 1,
  //   stagger: 0.1,
  // });
});
