function google_search(search_term) {
    var editChargerWindow = window.open('http://www.google.com/search?q='+search_term+'&tbm=isch', "", "width=700,height=620");
}

function print_qr() {
    /*
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'print_qr/', true);
    xhr.send();
    */
    var xhr = new XMLHttpRequest();
    if (confirm("Do you want to print in the office?")) {
        xhr.open('POST', 'print_qr/Godex_DT4x/', true);
    } else {
        xhr.open('POST', 'print_qr/Godex_g500/', true);
    }
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