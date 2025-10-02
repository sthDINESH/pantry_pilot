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

  /**
   * Shows toast for dynamic messages
   * @param {string} message
   * @param {string} type: "success", "danger", "info", "warning"
   */
  function showToast(message, type = "success") {
    // Create toast container if not present
    const toastContainer = document.querySelector(".toast-container");
    if (toastContainer) {
      // Create toast element
      const toast = document.createElement("div");
      toast.className = `toast align-items-center text-bg-${type} border-0 show`;
      toast.setAttribute("role", "alert");
      toast.setAttribute("aria-live", "assertive");
      toast.setAttribute("aria-atomic", "true");
      toast.innerHTML = `
      <div class="d-flex">
        <div class="toast-body">
          ${message}
        </div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
      `;
      toastContainer.appendChild(toast);

      new bootstrap.Toast(toast, { delay: 5000 }).show();

      // Remove toast from DOM after hidden
      toast.addEventListener("hidden.bs.toast", function () {
        toast.remove();
      });
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
  const baseModalTitle = document.querySelector("#base-modal .modal-title");
  const baseModalFooter = document.querySelector("#base-modal .modal-footer");

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

  // Create a BS5 modal object for meal plan modal if present
  // This modal is used in meals page to add/update a meal item
  // has an embedded form with CSRF token
  const mealPlanModalEl = document.querySelector("#meal-plan-modal");
  let mealPlanModal = null;
  if (mealPlanModalEl) {
    mealPlanModal = new bootstrap.Modal(mealPlanModalEl);
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
        const recipe = searchResults.find(
          (recipe) => recipe.api_recipe_id == recipeId
        );
        baseModalTitle.innerText = "Ingredients List";

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
    } else if (buttonType === "recipe-delete") {
      // Delete Saved Recipe
      button.addEventListener("click", function (event) {
        const recipeId = event.currentTarget.getAttribute("data-recipe-id");
        const recipeTitle =
          event.currentTarget.getAttribute("data-recipe-title");
        baseModalTitle.innerText = "Delete Recipe?";
        baseModalBody.innerHTML = `
            <p>
            Are you sure you want to delete <strong>${recipeTitle}</strong> from your recipes?
            <br>
            This action cannot be undone!
            </p>
        `;
        let deleteButton = document.querySelector("#recipe-delete");
        if (!deleteButton) {
          deleteButton = document.createElement("a");
          deleteButton.id = "recipe-delete";
          deleteButton.classList.add("btn", "btn-primary");
          deleteButton.innerText = "Delete";
          deleteButton.href = `/recipes/recipe/${recipeId}/delete`;
          baseModalFooter.appendChild(deleteButton);
        }
        baseModal.show();
      });
    } else if (buttonType === "toggle-meal-selection") {
      button.addEventListener("click", function (event) {
        event.preventDefault();
        const form = button.closest("form");
        const csrfTokenInput = form.querySelector(
          "input[name='csrfmiddlewaretoken']"
        );
        const csrfToken = csrfTokenInput ? csrfTokenInput.value : null;
        const recipeId = button.getAttribute("data-recipe-id");
        // AJAX call to update the server
        fetch(form.action, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
            "X-Requested-With": "XMLHttpRequest",
          },
          body: JSON.stringify({ recipe_id: recipeId }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              if (data.selected) {
                button.innerHTML =
                  '<i class="fa-solid fa-check"></i> Selected (Remove)';
              } else {
                button.innerHTML =
                  '<i class="fa-solid fa-calendar-plus"></i> Select for Meal Plan';
              }
            }
          })
          .catch((error) => {
            console.error("Error:", error);
          });
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

  // Recipes page - extract the tab parameter from URL
  // To support return to the same tab from where the details were viewed
  const urlParams = new URLSearchParams(window.location.search);
  const activeTab = urlParams.get("tab");

  if (activeTab) {
    // Map parameter values to actual tab IDs
    const tabMap = {
      discover: "discover-tab", // ?tab=discover → #discover-tab
      saved: "saved-tab", // ?tab=saved → #saved-tab
      "my-recipes": "my-recipes-tab", // ?tab=my-recipes → #my-recipes-tab
    };

    const tabId = tabMap[activeTab];
    if (tabId) {
      // Deactivate current active tab
      document
        .querySelectorAll("#recipes-form-tabs .nav-link")
        .forEach((tab) => {
          tab.classList.remove("active");
          tab.setAttribute("aria-selected", "false");
        });

      // Hide all tab content
      document
        .querySelectorAll("#recipes-section .tab-pane")
        .forEach((pane) => {
          pane.classList.remove("show", "active");
        });

      // Activate the target tab
      const targetTab = document.getElementById(tabId);
      const targetPane = document.getElementById(activeTab + "-pane");

      if (targetTab && targetPane) {
        targetTab.classList.add("active");
        targetTab.setAttribute("aria-selected", "true");
        targetPane.classList.add("show", "active");
      }
    }
  }

  // Initialize the toast for Django messages
  // This is BS5 requirement for toasts
  document.querySelectorAll(".toast").forEach(function (toastNode) {
    new bootstrap.Toast(toastNode, { delay: 5000 }).show();
  });

  // Full Calender objects to be rendered in meal planning page
  // Documentation: https://fullcalendar.io/docs
  // Renders two calender views:
  // - dayGridWeek/dayGridMonth: displays meal plan item days
  // - timeGridDay: displays meal plan item times
  // -------------------------------------------------------------------
  let calendarWeek = null; // dayGridWeek/dayGridMonth object
  let calendarDay = null; // timeGridDay object

  const calendarWeekEl = document.getElementById("calendar-week");
  if (calendarWeekEl) {
    calendarWeek = new FullCalendar.Calendar(calendarWeekEl, {
      headerToolbar: {
        start: "prev, next, today",
        center: "title",
        end: "dayGridWeek,dayGridMonth",
      },
      aspectRatio: 3.5,
      themeSystem: "bootstrap5",
      initialView: "dayGridWeek",
      slotMinTime: "06:00:00",
      slotMaxTime: "24:00:00",
      slotDuration: "6:00:00",
      expandRows: true,
      allDaySlot: false,
      events: "/meals/plan/",
      eventDisplay: "block",
      eventClick: calendarWeekEventClick,
      dateClick: calendarWeekDateClick,
    });
    calendarWeek.render();
  }

  const calendarDayEl = document.getElementById("calendar-day");
  if (calendarDayEl) {
    calendarDay = new FullCalendar.Calendar(calendarDayEl, {
      headerToolbar: {
        start: "",
        center: "title",
        end: "",
      },
      themeSystem: "bootstrap5",
      initialView: "timeGridDay",
      slotMinTime: "06:00:00",
      slotMaxTime: "24:00:00",
      slotDuration: "03:00:00",
      expandRows: true,
      allDaySlot: false,
      selectable: true,
      selectMirror: true,
      events: "/meals/plan/",
      eventMinHeight: 40,

      eventClick: function (info) {
        // Handle meal click
        console.log("Meal clicked:", info.event);
      },

      dateClick: calendarDayDateClick,

      select: calendarDaySelect,
    });
    calendarDay.render();
  }

  // Register an event handler to the today button in dayGridWeek/dayGridMonth view
  // to move the timeGridDay view to today's date in sync
  // timeout is required to allow the objects to completely render
  setTimeout(function () {
    const todayBtn =
      calendarWeekEl.parentNode.querySelector(".fc-today-button");
    if (todayBtn) {
      todayBtn.addEventListener("click", function () {
        if (calendarDay) {
          calendarDay.today(); // Move day view to today
        }
      });
    }
  }, 0);

  // Calender callbacks
  // ------------------
  /**
   * Callback function for week/Month view calendar's dateClick event
   * Documentation: https://fullcalendar.io/docs
   * @param {dateClickInfo} info
   */
  function calendarWeekDateClick(info) {
    // If in dayGridMonth view, change to dayGridWeek view
    calendarWeek.changeView("dayGridWeek", info.date);
    // Move the day view calender to the selected date
    if (calendarDay) {
      calendarDay.gotoDate(info.date);
    }
  }

  /**
   * Callback function for week/Month view calendar's eventClick event
   * Documentation: https://fullcalendar.io/docs
   * @param {eventClickInfo} info
   */
  function calendarWeekEventClick(info) {
    // Change the day view calender to show the day of the event
    calendarDay.goto(info.date);
    // TODO: show modal to update an event
  }

  /**
   * Callback function for timeGridDay view calendar's select event
   * Documentation: https://fullcalendar.io/docs
   * @param {selectionInfo} info
   */
  function calendarDaySelect(info) {
    // If selection is a single click (not a drag), 
    // adjust end time to 3 hours after start
    const start = info.start;
    let end = info.end;

    // If duration is 1 hour, adjust to 3 hours
    if (end - start === 60 * 60 * 1000) {
      end = new Date(start.getTime() + 3 * 60 * 60 * 1000);
      info.end = end;
    }
    createNewEvent(info);
  }

  /**
   * Callback function for timeGridDay view calendar's dateClick event
   * Documentation: https://fullcalendar.io/docs
   * @param {dateClickInfo} info
   */
  function calendarDayDateClick(info) {}

  /**
   * Function to pop-up modal with form for meal plan item object creation
   * Uses info.start and info.end properties to pre-populate the form fields
   * Processes JS datetime object to Django's default format
   * @param {selectionInfo} info
   */
  function createNewEvent(info) {
    const mealPlanModalTitle = document.querySelector(
      "#meal-plan-modal .modal-title"
    );
    mealPlanModalTitle.innerText = "Add new meal to plan?";
    const mealStartTime = document.querySelector("#id_start_time");
    const mealEndTime = document.querySelector("#id_end_time");

    if (mealStartTime) {
      mealStartTime.value = info.start
        .toISOString() // toISOString() returns 2025-10-02T21:00:00.000Z
        .slice(0, 19) // .slice(0, 19) removes milliseconds and timezone
        .replace("T", " "); // converts to Django's default format
    }

    if (mealEndTime) {
      mealEndTime.value = info.end.toISOString().slice(0, 19).replace("T", " ");
    }
    mealPlanModal.show();
  }

  // Event handler for the submit action for the form meal plan modal
  // AJAX post request is sent to the server with the form data from the modal
  // This keeps the server in sync without having to re-render the page(better UX)
  // Updates the calendar views without page re-fresh
  const mealPlanForm = mealPlanModalEl.querySelector("form");

  if (mealPlanForm) {
    mealPlanForm.addEventListener("submit", function (event) {
      event.preventDefault();

      const formData = new FormData(mealPlanForm);

      // AJAX POST request to update the server
      fetch(mealPlanForm.action, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            // Success: close modal, show toast, update calendar, etc.
            bootstrap.Modal.getInstance(mealPlanModalEl).hide();
            showToast(data.message, "success");
            calendarDay.refetchEvents();
            calendarWeek.refetchEvents();
          } else {
            bootstrap.Modal.getInstance(mealPlanModalEl).hide();
            showToast(data.message, "danger");
          }
        })
        .catch((error) => {
          console.error("AJAX error:", error);
        });
    });
  }

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
