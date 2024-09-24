const $addPetModal = document.querySelector("#add-pet-modal");
const $addPetBtn = document.querySelector("#add-pet-btn");

const toggleFieldMessage = (field, message) => {
  const $field = document.querySelector(`#${field}-message`);

  if ($field) {
    $field.style.display = message ? "block" : "none";
    $field.textContent = message;
  }
};

function onConfirmPet() {
  const $photo = document.forms["add-pet"]["photo"];

  const form = {
    name: document.forms["add-pet"]["name"].value,
    weight: document.forms["add-pet"]["weight"].value,
    species: document.forms["add-pet"]["species"].value,
    birthday: document.forms["add-pet"]["birthday"].value,
    photo: $photo.files[0],
  };

  const formData = new FormData();

  for (const field in form) {
    if (!form[field] && field !== "photo") {
      return toggleFieldMessage(field, "This field is required.");
    }

    toggleFieldMessage(field);
    formData.append(field, form[field]);
  }

  fetch("/add-pet", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (response.ok) {
        alert("The pet was added");

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

$addPetModal.addEventListener("show.bs.modal", () => {
  document.forms["add-pet"]["name"].value = "";
  document.forms["add-pet"]["weight"].value = undefined;
  document.forms["add-pet"]["species"].value = "";
  document.forms["add-pet"]["birthday"].value = undefined;
  document.forms["add-pet"]["photo"].value = "";

  toggleFieldMessage("name");
  toggleFieldMessage("weight");
  toggleFieldMessage("species");
  toggleFieldMessage("birthday");

  $addPetBtn.addEventListener("click", onConfirmPet);
});

$addPetModal.addEventListener("hidden.bs.modal", () => {
  $addPetBtn.removeEventListener("click", onConfirmPet);
});
