function google_search(search_term) {
    var editChargerWindow = window.open('http://www.google.com/search?q='+search_term+'&tbm=isch', "", "width=700,height=620");
}

/*
function print_qr() {
    var xhr = new XMLHttpRequest();
    if (confirm("Do you want to print in the office?")) {
        xhr.open('POST', 'print_qr/Godex_DT4x/', true);
    } else {
        xhr.open('POST', 'print_qr/Godex_G500/', true);
    }
    xhr.send();
}
*/

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
    URLtoWorkWith = location.href;
    parts = URLtoWorkWith.split('/')
    for (var i =0; i<3; i++) {
		parts.pop();
	}
    var editWindow = window.open(parts.join('/')+'/edit_order/'+index+'/', "", "width=1000,height=650");
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

function load() {
    setInputFilter(document.getElementById("intTextBox"), function(value) { return /^-?\d*$/.test(value); });
    setInputFilter(document.getElementById("coreCount"), function(value) { return /^-?\d*$/.test(value); });
    setInputFilter(document.getElementById("threadCount"), function(value) { return /^-?\d*$/.test(value); });
}

window.onload = function() {load()}

function open_drive_edit(index) {
    URLtoWorkWith = location.href;
    parts = URLtoWorkWith.split('/')
    for (var i =0; i<3; i++) {
		parts.pop();
	}
	var driveEditWindow = window.open(parts.join('/')+'/hdd_edit/'+index+'/', "", "width=400,height=650");
}

function search_observation() {

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
    //parent.style.display = "none";
    $(id).toggle('fast');
}
window.addEventListener('load', function () {
    var els = document.querySelectorAll('.modaljs');
    for (var i = 0; i < els.length; i++) {
        //els[i].style.display = "none";
    }
});