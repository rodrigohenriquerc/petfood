const $addMealModal = document.querySelector("#add-meal-modal");
const $confirmMealBtn = document.querySelector("#confirm-meal");
const $petMessage = document.querySelector("#pet-message");
const $quantityMessage = document.querySelector("#quantity-message");

const togglePetMessage = (message) => {
  $petMessage.style.display = message ? "block" : "none";
  $petMessage.textContent = message;
};

const toggleQuantityMessage = (message) => {
  $quantityMessage.style.display = message ? "block" : "none";
  $quantityMessage.textContent = message;
};

const onConfirmMeal = () => {
  let isFormValid = true;

  const pet_id = document.forms["add-meal"]["pet_id"].value;
  const quantity = document.forms["add-meal"]["quantity"].value;

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

  if (isFormValid) {
    fetch("/add-meal", {
      method: "POST",
      body: JSON.stringify({ pet_id, quantity }),
      headers: { "Content-Type": "application/json" },
    })
      .then((response) => {
        if (response.ok) {
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
};

$addMealModal.addEventListener("show.bs.modal", () => {
  document.forms["add-meal"]["pet_id"].value = undefined;
  document.forms["add-meal"]["quantity"].value = undefined;

  togglePetMessage();
  toggleQuantityMessage();

  $confirmMealBtn.addEventListener("click", onConfirmMeal);
});

$addMealModal.addEventListener("hidden.bs.modal", () => {
  $confirmMealBtn.removeEventListener("click", onConfirmMeal);
});
