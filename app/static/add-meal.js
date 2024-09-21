const $addMealModal = document.querySelector("#add-meal-modal");
const $confirmMealBtn = document.querySelector("#confirm-meal");
const $petRequiredMessage = document.querySelector("#pet-required-message");
const $quantityRequiredMessage = document.querySelector(
  "#quantity-required-message"
);
const $quantityInvalidMessage = document.querySelector(
  "#quantity-invalid-message"
);

const setPetRequiredMessageDisplay = (display) => {
  $petRequiredMessage.style.display = display;
};

const setQuantityRequiredMessageDisplay = (display) => {
  $quantityRequiredMessage.style.display = display;
};

const setQuantityInvalidMessageDisplay = (display) => {
  $quantityInvalidMessage.style.display = display;
};

const onConfirmMeal = () => {
  let isFormValid = true;

  const pet_id = document.forms["add-meal"]["pet_id"].value;
  const quantity = document.forms["add-meal"]["quantity"].value;

  if (!pet_id) {
    setPetRequiredMessageDisplay("block");
    isFormValid = false;
  } else {
    setPetRequiredMessageDisplay("none");
  }

  if (!quantity) {
    setQuantityRequiredMessageDisplay("block");
    isFormValid = false;
  } else if (quantity <= 0) {
    setQuantityInvalidMessageDisplay("block");
    isFormValid = false;
  } else {
    setQuantityRequiredMessageDisplay("none");
    setQuantityInvalidMessageDisplay("none");
  }

  if (isFormValid) {
    fetch("/add-meal", {
      method: "POST",
      body: JSON.stringify({ pet_id, quantity }),
      headers: { "Content-Type": "application/json" },
    })
      .then((response) => {
        if (response.ok) {
          window.location.reload();
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
};

$addMealModal.addEventListener("show.bs.modal", () => {
  document.forms["add-meal"]["pet_id"].value = undefined;
  document.forms["add-meal"]["quantity"].value = undefined;

  setPetRequiredMessageDisplay("none");
  setQuantityRequiredMessageDisplay("none");
  setQuantityInvalidMessageDisplay("none");

  $confirmMealBtn.addEventListener("click", onConfirmMeal);
});

$addMealModal.addEventListener("hidden.bs.modal", () => {
  $confirmMealBtn.removeEventListener("click", onConfirmMeal);
});
