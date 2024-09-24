const $removePetModal = document.querySelector("#remove-pet-modal");
const $removePetBtn = document.querySelector("#remove-pet-btn");

document
  .querySelectorAll("#resource-actions [data-bs-target='#remove-pet-modal']")
  .forEach((el) => {
    el.addEventListener("click", function () {
      const petId = this.dataset.petid;

      $removePetBtn.setAttribute("data-petid", petId);
    });
  });

function onConfirmRemoveMeal() {
  const petId = this.dataset.petid;

  fetch(`/remove-pet/${petId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  })
    .then((response) => {
      if (response.ok) {
        alert("The pet was removed");

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

$removePetModal.addEventListener("show.bs.modal", function () {
  $removePetBtn.addEventListener("click", onConfirmRemoveMeal);
});

$removePetModal.addEventListener("hidden.bs.modal", () => {
  $removePetBtn.removeEventListener("click", onConfirmRemoveMeal);
});
