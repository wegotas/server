function alertbox() {
  alert('Edit placeholder')
}

function edit(button, id) {

  field = document.getElementById(id);
  if (field.readOnly) {
    console.log("True");
    button.innerText = "Save";
    field.classList.remove("greyed");
    field.readOnly = false;
  } else {
    console.log("False");
    button.innerText = "Edit";
    field.classList.add("greyed");
    field.readOnly = true;
  }
}
