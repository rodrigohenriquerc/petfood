const $removeMealModal = document.querySelector("#remove-meal-modal");
const $removeMealConfirmationBtn = document.querySelector(
  "#remove-meal-confirmation-btn"
);
const $removeMealOpenModalBtns = document.querySelectorAll(
  "#resource-actions [data-bs-target='#remove-meal-modal']"
);

$removeMealOpenModalBtns.forEach((el) => {
  el.addEventListener("click", function () {
    const mealId = this.dataset.mealid;

    $removeMealConfirmationBtn.setAttribute("data-mealid", mealId);
  });
});

function onConfirmRemoveMeal() {
  const mealId = this.dataset.mealid;

  fetch(`/remove-meal/${mealId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  })
    .then((response) => {
      if (response.ok) {
        alert("The meal was removed");

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

$removeMealModal.addEventListener("show.bs.modal", function () {
  $removeMealConfirmationBtn.addEventListener("click", onConfirmRemoveMeal);
});

$removeMealModal.addEventListener("hidden.bs.modal", () => {
  $removeMealConfirmationBtn.removeEventListener("click", onConfirmRemoveMeal);
});
