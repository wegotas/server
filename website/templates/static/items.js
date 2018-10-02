function edit(button, id) {
  field = id;
  if (field.readOnly) {
    console.log("True");
    button.innerText = "Save";
    field.classList.remove("greyed");
    field.readOnly = false;
  } else {
    console.log("False");
    button.innerText = "Edit";
    field.classList.add("greyed");
    /*
    console.log(field.value);
    */
    sendEditedItem(field.id.replace("field", ""), field.value);
    field.readOnly = true;
  }
}

function sendEditedItem(ItemId, ItemName) {
  console.log(ItemId);
  console.log(ItemName);
  var xhr = new XMLHttpRequest();
  var objectToSend = {};
  objectToSend["ItemId"] = ItemId;
  objectToSend["ItemName"] = ItemName;
  object = JSON.stringify(objectToSend);
  xhr.open('POST', 'edit/', true);
  xhr.send(object);
  xhr.onreadystatechange = function(e) {
    if (xhr.readyState === 4) {
      console.log("Edit sent");
    }
  }
}

function deleteItem(ItemId) {
  if (confirm("Do you really want do delete this object?")) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'del/'+ItemId+'/', true);
    xhr.send();
    xhr.onreadystatechange = function(e) {
      if (xhr.readyState === 4) {
        location.reload();
      }
    }
  }
}

