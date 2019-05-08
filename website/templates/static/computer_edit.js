function get_main_url() {
    parts = location.href.split('/')
    for (var i = 0; i<3; i++) {
		parts.pop();
	}
	return parts.join('/');
}

function google_search(search_term) {
    var editChargerWindow = window.open('http://www.google.com/search?q='+search_term+'&tbm=isch', "", "width=700,height=620");
}

function print_qr_with_printer(printer) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'print_qr/' + printer + '/', true);
    xhr.send();
}

function toggle_visibility(button) {
    section = button.parentElement.parentElement.getElementsByClassName('section-member')[0];
    section.classList.toggle('hidden');
}

function open_order(index) {
    var editWindow = window.open(get_main_url()+'/edit_order/'+index+'/', "", "width=1000,height=650");
}

function setInputFilter(textbox, inputFilter) {
    ["input", "keydown", "keyup", "mousedown", "mouseup", "select", "contextmenu", "drop"].forEach(function(event) {
        textbox.addEventListener(event, function() {
            if (inputFilter(this.value)) {
                this.oldValue = this.value;
                this.oldSelectionStart = this.selectionStart;
                this.oldSelectionEnd = this.selectionEnd;
            } else if (this.hasOwnProperty("oldValue")) {
                this.value = this.oldValue;
                this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
            }
        });
    });
}

function wait(ms) {
    var d = new Date();
    var d2 = null;
    do { d2 = new Date(); }
    while(d2-d < ms);
}

function load() {
    setInputFilter(document.getElementById("intTextBox"), function(value) { return /^-?\d*$/.test(value); });
    setInputFilter(document.getElementById("coreCount"), function(value) { return /^-?\d*$/.test(value); });
    setInputFilter(document.getElementById("threadCount"), function(value) { return /^-?\d*$/.test(value); });
    observationSearchBox = document.getElementById("observation-search-box")
    observationSearchBox.addEventListener('keypress', function(event) {
        if ((event.keyCode === 13) && (keyword_suitable_for_search(observationSearchBox.value))) {
            search_observation(observationSearchBox.value);
            event.preventDefault();
        }
    })
}

function keyword_suitable_for_search(keyword) {
    // checks if keyword is empty
    if (keyword  === '') {
        return false;
    }
    // checks if whole keyword consists only of space characters
    if (keyword.split(' ').join('').length === 0) {
        return false;
    }
    return true
}

window.onload = function() {load()}

function open_drive_edit(index) {
	var driveEditWindow = window.open(get_main_url()+'/hdd_edit/'+index+'/', "", "width=400,height=650");
}

function search_observation(keyword) {
    observation_result_toggler = document.getElementById("observation_result_toggler");
    observation_adder = document.getElementById("observation-adder");
    var xhr = new XMLHttpRequest();
    computer_id = document.getElementById("computer_id").value
    xhr.open('GET', get_main_url() + '/observations_to_add/' + computer_id + '/' + urlify(keyword) + '/', true)
    xhr.send();
    xhr.onreadystatechange = function(e) {
        if (xhr.readyState === 4) {
            observation_adder.classList.remove("hidden");
            observation_result_toggler.classList.remove('hidden');
            observation_adder.innerHTML = xhr.responseText;
        }
    }
}

function add_observation(button, observation_id) {
    computer_id = document.getElementById("computer_id").value;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', get_main_url() + '/assign_observation_to_computer/' + observation_id + '/' + computer_id + '/');
    xhr.send();
    holder_of_observations = document.getElementById("holder_of_observations");
    xhr.onreadystatechange = function(e) {
        if (xhr.readyState === 4) {
            if (xhr.status == 200) {
                row = button.parentNode.parentNode;
                table = document.getElementById("observation-search-results");
                row.parentNode.removeChild(row);
                holder_of_observations.innerHTML += xhr.responseText;
            }
            else {
                alert(xhr.responseText);
            }
        }
    }
}

function toggle_observation_results() {
    document.getElementById("observation-adder").classList.toggle("hidden");
}

function modaljs(id, closeable) {
    var body = document.querySelector("body");
    var parent = document.querySelector(id);
    parent.classList.toggle('on');
    var bg = document.createElement("div");
    var close = document.createElement("div");
    bg.className = "modal-js-overlay";
    close.className = "modal-js-close";

    var godex_dt4x_printer_button = document.createElement("button");
    godex_dt4x_printer_button.innerHTML = "Print in office (Godex_DT4x)";
    godex_dt4x_printer_button.type = "button";
    godex_dt4x_printer_button.display = "block";

    var godex_g500_printer_button = document.createElement("button");
    godex_g500_printer_button.innerHTML = "Print in warehouse (Godex_G500)";
    godex_g500_printer_button.type = "button";
    godex_g500_printer_button.display = "block";

    if (closeable) {
        close.innerHTML = "x";
        close.addEventListener('click', function () {
            var overlay = body.querySelector(".modal-js-overlay");
            var closebtn = parent.querySelector(".modal-js-close");
            body.removeChild(overlay);
            parent.classList.toggle('on');
            parent.removeChild(closebtn);
            parent.removeChild(godex_dt4x_printer_button);
            parent.removeChild(godex_g500_printer_button);
        });
        parent.appendChild(close);
    }
    body.appendChild(bg);

    godex_dt4x_printer_button.addEventListener('click', function () {
        print_qr_with_printer("Godex_DT4x");
        var overlay = body.querySelector(".modal-js-overlay");
        var closebtn = parent.querySelector(".modal-js-close");
        body.removeChild(overlay);
        parent.classList.toggle('on');
        parent.removeChild(closebtn);
        parent.removeChild(godex_dt4x_printer_button);
        parent.removeChild(godex_g500_printer_button);
    });
    parent.appendChild(godex_dt4x_printer_button);

    godex_g500_printer_button.addEventListener('click', function () {
        print_qr_with_printer("Godex_G500");
        var overlay = body.querySelector(".modal-js-overlay");
        var closebtn = parent.querySelector(".modal-js-close");
        body.removeChild(overlay);
        parent.classList.toggle('on');
        parent.removeChild(closebtn);
        parent.removeChild(godex_dt4x_printer_button);
        parent.removeChild(godex_g500_printer_button);
    });
    parent.appendChild(godex_g500_printer_button);
}

function modaljsoff(id) {
    var body = document.querySelector("body");
    var parent = document.querySelector(id);
    var overlay = body.querySelector(".modal-js-overlay");
    var closebtn = parent.querySelector(".modal-js-close");
    body.removeChild(overlay);
    parent.classList.toggle('on');
}

window.addEventListener('load', function () {
    var els = document.querySelectorAll('.modaljs');
    for (var i = 0; i < els.length; i++) {
        //els[i].style.display = "none";
    }
});

function urlify (url) {
    urlToReturn = url.split('#').join('%23');
    return urlToReturn;
}

function remove_drive_from_computer(button, computer_id, drive_id) {
    remove_object_from_computer(button, computer_id, drive_id, 'remove_drive_from_computer')
}

function remove_observation_from_computer(button, computer_id, observation_id) {
    remove_object_from_computer(button, computer_id, observation_id, 'remove_observation_from_computer')
}

function remove_ramstick_from_computer(button, computer_id, ramstick_id) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', get_main_url() + '/remove_ramstick_from_computer/' + ramstick_id + '/' + computer_id + '/');
    xhr.send();
    xhr.onreadystatechange = function(e) {
        if (xhr.readyState === 4) {
            if (xhr.status == 200) {
                section = button.parentNode.parentNode;
                element_to_remove = button.parentNode;
                section.removeChild(element_to_remove);
                section.innerHTML += xhr.responseText;
            }
            else {
                alert(xhr.responseText);
            }
        }
    }
}

function remove_object_from_computer(button, computer_id, object_id, url_part) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', get_main_url() + '/' + url_part + '/' + object_id + '/' + computer_id + '/');
    xhr.send();
    xhr.onreadystatechange = function(e) {
        if (xhr.readyState === 4) {
            if (xhr.status == 200) {
                table_holder = button.parentNode;
                table_holder.parentNode.removeChild(table_holder);
            }
            else {
                alert(xhr.responseText);
            }
        }
    }
}

function AddNonExistantRamstick(button, computer_id) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', get_main_url() + '/add_nonexistant_ramstick/' + computer_id + '/');
    xhr.send();
    xhr.onreadystatechange = function(e) {
        if (xhr.readyState === 4) {
            if (xhr.status == 200) {
                button.parentNode.parentNode.innerHTML += xhr.responseText;
            }
            else {
                alert(xhr.responseText);
            }
        }
    }
}