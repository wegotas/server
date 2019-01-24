window.onload = function() {load()}
var selected_serials = [];

function toggleDetails() {
    var button = document.getElementById("detail-button");
    var details = document.getElementsByClassName('detail');
    if (button.innerHTML.includes("Show")) {
        button.innerHTML = "&nbsp;&#8639; Hide details &#8639;&nbsp;";
        display = "table-row";
    } else {
        button.innerHTML = "&nbsp;&#8643; Show more details &#8642;&nbsp;";
        display = 'none';
    }
    for (detail of details) {
        detail.style.display = display;
    }
}

function load() {
    searchbox = document.getElementById('searchbox');
    if (searchbox) {
        searchbox.addEventListener('keyup', function(event) {
            event.preventDefault();
            search_using_keyword();
        })
    }
    checkboxes = document.getElementsByClassName('record-chkbx');
    for (checkbox of checkboxes) {
        checkbox.checked = false;
    }
}

function search_using_keyword() {
    keyword = document.getElementById('searchbox').value;
    chargerContainers = document.getElementsByClassName("charger-container");
    for (container of chargerContainers) {
        chargerSerial = container.getElementsByClassName("charger-serial")[0].value;
        if (chargerSerial.includes(keyword)) {
            container.style.display = "block";
        } else {
            container.style.display = "none";
        }
    }
}

function toggleDisabled(button, index) {
    button.innerHTML.includes()
    inputbox = button.parentElement.parentElement.getElementsByClassName('charger-serial')[0];
    if (inputbox.disabled) {
        inputbox.disabled = false;
        button.innerHTML= 'Save';
    } else {
        serial = inputbox.value
        var xhr = new XMLHttpRequest();
        var objectToSend = {};
        objectToSend["Index"] = index;
        objectToSend["Serial"] = serial;
        object = JSON.stringify(objectToSend);
        xhr.open('POST', 'edit/', true);
        xhr.send(object);
        xhr.onreadystatechange = function(e) {
            if (xhr.readyState === 4) {
                console.log("Edit sent");
            }
        }
        inputbox.disabled = true;
        button.innerHTML= 'Edit&nbsp;';
    }
}

function printQR(index) {
    var xhr = new XMLHttpRequest();
    var objectToSend = {};
    objectToSend["Index"] = index;
    object = JSON.stringify(objectToSend);
    xhr.open('POST', 'print/', true);
    xhr.send(object);
    xhr.onreadystatechange = function(e) {
        if (xhr.readyState === 4) {
            console.log("sent");
        }
    }
}

function deleteCharger(index) {
    var xhr = new XMLHttpRequest();
    var objectToSend = {};
    objectToSend["Index"] = index;
    object = JSON.stringify(objectToSend);
    xhr.open('POST', 'delete/', true);
    xhr.send(object);
    xhr.onreadystatechange = function(e) {
      if (xhr.readyState === 4) {
        location.reload();
      }
    }
}

function serialSelect(checkbox) {
    if (checkbox.checked){
        selected_serials.push(checkbox.value);
    } else {
        selected_serials.splice(selected_serials.indexOf(checkbox.value), 1);
    }
    if (selected_serials.length>0) {
      document.getElementById("printButton").style.display = "inline-block";
    } else {
      document.getElementById("printButton").style.display = "none";
    }
}

function selectAllSerials(checkbox) {
    checkboxes = document.getElementsByClassName('record-chkbx');
    for (chckbx of checkboxes) {
        if (chckbx.parentElement.parentElement.style.display != 'none'){
            chckbx.checked = checkbox.checked;
        }
    }
}

function printSelectedSerials() {
    var xhr = new XMLHttpRequest();
    object = JSON.stringify(selected_serials);
    xhr.open('POST', 'print_serials/', true);
    xhr.send(object);
}

