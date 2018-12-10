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

function edit_details(button, id, shotcode_field, fullname_field) {
    if (fullname_field.readOnly) {
        button.innerText = "Save";
        shotcode_field.classList.remove("greyed");
        fullname_field.classList.remove("greyed");
        shotcode_field.readOnly = false;
        fullname_field.readOnly = false;
    } else {
        button.innerText = "Edit";
        shotcode_field.classList.add("greyed");
        fullname_field.classList.add("greyed");
        shotcode_field.readOnly = true;
        fullname_field.readOnly = true;
        var xhr = new XMLHttpRequest();
        var objectToSend = {};
        objectToSend['observation_id'] = id;
        objectToSend['shortcode'] = shotcode_field.value;
        objectToSend['fullname'] = fullname_field.value;
        object = JSON.stringify(objectToSend);
        xhr.open('POST', 'edit/', true);
        xhr.send(object);
        xhr.onreadystatechange = function(e) {
        if (xhr.readyState === 4) {
            console.log("Edit sent");
        }
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

function revealSubcategories(button, categoryclassname) {
    var buttons = document.getElementsByClassName('category');
    for (category_button of buttons) {
        category_button.classList.remove('red');
    }
    var buttons = document.getElementsByClassName('subcategory');
    for (category_button of buttons) {
        category_button.classList.remove('red');
    }
    button.classList.add('red');
    var area = document.getElementsByClassName('details');
    var elements1 = area[0].getElementsByClassName('hideable');
    for (element of elements1) {
        element.classList.add('hidden');
    }

    var elements2 = area[1].getElementsByClassName('hideable');
    for (element of elements2) {
        element.classList.add('hidden');
    }

    var elements3 = document.getElementsByClassName('actions')[0].getElementsByClassName('hideable');
    for (element of elements3) {
        element.classList.add('hidden');
    }

    var area = document.getElementsByClassName('subcategories')[0];
    var elements = area.getElementsByClassName('hideable');
    for (element of elements) {
        if (element.classList.contains(categoryclassname)) {
            element.classList.remove('hidden');
        } else {
            element.classList.add('hidden');
        }
    }
}

function revealShortcodes(button, categoryclassname, subcategoryclassname) {
    var buttons = document.getElementsByClassName('subcategory');
    for (category_button of buttons) {
        category_button.classList.remove('red');
    }
    button.classList.add('red');
    var area = document.getElementsByClassName('details');
    var elements1 = area[0].getElementsByClassName('hideable');
    for (element of elements1) {
        if (element.classList.contains(categoryclassname) && element.classList.contains(subcategoryclassname)) {
            element.classList.remove('hidden');
        } else {
            element.classList.add('hidden');
        }
    }
    var elements2 = area[1].getElementsByClassName('hideable');
    for (element of elements2) {
        if (element.classList.contains(categoryclassname) && element.classList.contains(subcategoryclassname)) {
            element.classList.remove('hidden');
        } else {
            element.classList.add('hidden');
        }
    }
    var elements3 = document.getElementsByClassName('actions')[0].getElementsByClassName('hideable');
    for (element of elements3) {
        if (element.classList.contains(categoryclassname) && element.classList.contains(subcategoryclassname)) {
            element.classList.remove('hidden');
        } else {
            element.classList.add('hidden');
        }
    }
}