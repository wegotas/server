function google_search(search_term) {
    var editChargerWindow = window.open('http://www.google.com/search?q='+search_term+'&tbm=isch', "", "width=700,height=620");
}

function print_qr() {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'print_qr/', true);
    xhr.send();
}

function toggle_visibility(button) {
    section = button.parentElement.parentElement.getElementsByClassName('section-member')[0];
    section.classList.toggle('hidden');
}

function open_order(index) {
    console.log(index);
    URLtoWorkWith = location.href;
    console.log(URLtoWorkWith);
    parts = URLtoWorkWith.split('/')
    for (var i =0; i<3; i++) {
		parts.pop();
	}
    var editWindow = window.open(parts.join('/')+'/edit_order/'+index+'/', "", "width=1000,height=650");
}