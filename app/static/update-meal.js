const $updateMealModal = document.querySelector("#update-meal-modal");
const $updateMealConfirmationBtn = document.querySelector(
  "#update-meal-confirmation-btn"
);
const $petMessage = document.querySelector("#pet-message");
const $quantityMessage = document.querySelector("#quantity-message");

const $updateMealOpenModalBtns = document.querySelectorAll(
  "#resource-actions [data-bs-target='#update-meal-modal']"
);

$updateMealOpenModalBtns.forEach((el) => {
  el.addEventListener("click", function () {
    const mealId = this.dataset.mealid;
    const pet_id = this.dataset.pet;
    const quantity = this.dataset.quantity;

    $updateMealConfirmationBtn.setAttribute("data-mealid", mealId);
    $updateMealModal.setAttribute("data-pet", pet_id);
    $updateMealModal.setAttribute("data-quantity", quantity);
  });
});

const togglePetMessage = (message) => {
  $petMessage.style.display = message ? "block" : "none";
  $petMessage.textContent = message;
};

const toggleQuantityMessage = (message) => {
  $quantityMessage.style.display = message ? "block" : "none";
  $quantityMessage.textContent = message;
};

function onConfirmMeal() {
  let isFormValid = true;

  const pet_id = document.forms["update-meal"]["pet_id"].value;
  const quantity = document.forms["update-meal"]["quantity"].value;

  if (!pet_id) {
    togglePetMessage("Pet is required.");
    isFormValid = false;
  } else {
    togglePetMessage();
  }

  if (!quantity) {
    toggleQuantityMessage("Quantity is required.");
    isFormValid = false;
  } else if (quantity <= 0) {
    toggleQuantityMessage("Quantity must be more than 0.");
    isFormValid = false;
  } else {
    toggleQuantityMessage();
  }

  const mealId = this.dataset.mealid;

  if (isFormValid) {
    fetch(`/update-meal/${mealId}`, {
      method: "POST",
      body: JSON.stringify({ pet_id, quantity }),
      headers: { "Content-Type": "application/json" },
    })
      .then((response) => {
        if (response.ok) {
          alert("The meal was updated");

          return window.location.reload();
        }

        return response.json();
      })
      .then((data) => {
        alert(data.message);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
}

$updateMealModal.addEventListener("shown.bs.modal", function () {
  document.forms["update-meal"]["pet_id"].value = this.dataset.pet;
  document.forms["update-meal"]["quantity"].value = this.dataset.quantity;

  togglePetMessage();
  toggleQuantityMessage();

  $updateMealConfirmationBtn.addEventListener("click", onConfirmMeal);
});

$updateMealModal.addEventListener("hidden.bs.modal", () => {
  $updateMealConfirmationBtn.removeEventListener("click", onConfirmMeal);
});
