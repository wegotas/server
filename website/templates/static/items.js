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
        sendEditedItem(field.id.replace("field", ""), field.value);
        field.readOnly = true;
    }
}

function sendEditedItem(ItemId, ItemName) {
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

function showSubcategories(button, categoryClassname) {
    // Removes red highlight from category buttons.
    var buttons = document.getElementsByClassName('category');
    for (category_button of buttons) {
        category_button.classList.remove('red');
    }

    // Removes red highlight from subcategory buttons.
    var buttons = document.getElementsByClassName('subcategory');
    for (category_button of buttons) {
        category_button.classList.remove('red');
    }
    // Adds red highlight to category button.
    button.classList.add('red');

    // Hides observation details.
    var details = document.getElementsByClassName('detail');
    for (detail_div of details) {
        detail_div.classList.add('hidden');
    }

    // Hides divs which are do not fulfill categoryClassname criteria, and shows which do.
    var subcategoriesDiv = document.getElementsByClassName('subcategories')[0];
    var subcategoryDivs = subcategoriesDiv.getElementsByClassName('hideable');
    for (subcategoryDiv of subcategoryDivs) {
        if (subcategoryDiv.classList.contains(categoryClassname)) {
            subcategoryDiv.classList.remove('hidden');
        } else {
            subcategoryDiv.classList.add('hidden');
        }
    }
}

function showDetails(button, categoryClassname, subcategoryClassname) {
    // Adds red highlight to subcategory button.
    var buttons = document.getElementsByClassName('subcategory');
    for (category_button of buttons) {
        category_button.classList.remove('red');
    }
    button.classList.add('red');

    // Shows details having category class name and subcategory class name. Hides the rest.
    var area = document.getElementsByClassName('details');
    var elements1 = area[0].getElementsByClassName('hideable');
    for (element of elements1) {
        if (element.classList.contains(categoryClassname) && element.classList.contains(subcategoryClassname)) {
            element.classList.remove('hidden');
        } else {
            element.classList.add('hidden');
        }
    }
}

function change_readonly_status(object, status) {
    /* Changes readonly status of an oject and changes it's colour(grey/white). */
    object.readOnly = status;
    if (status) {
        object.classList.remove("whited");
        object.classList.add("greyed");
    } else {
        object.classList.remove("greyed");
        object.classList.add("whited");
    }
}

function edit_detail(button, id) {
    shortcode_field = document.getElementById('shortcode'+id);
    fullname_field = document.getElementById('fullname'+id);
    is_readonly = fullname_field.readOnly;
    if (fullname_field.readOnly) {
        button.innerText = "Save";
        change_readonly_status(shortcode_field, !is_readonly);
        change_readonly_status(fullname_field, !is_readonly);
    } else {
        button.innerText = "Edit";
        change_readonly_status(shortcode_field, !is_readonly);
        change_readonly_status(fullname_field, !is_readonly);
        var xhr = new XMLHttpRequest();
        var objectToSend = {};
        objectToSend['observation_id'] = id;
        objectToSend['shortcode'] = shortcode_field.value;
        objectToSend['fullname'] = fullname_field.value;
        object = JSON.stringify(objectToSend);
        xhr.open('POST', 'edit/', true);
        xhr.send(object);
    }
}