function google_search(search_term) {
    var editChargerWindow = window.open('http://www.google.com/search?q='+search_term+'&tbm=isch', "", "width=700,height=620");
}

function print_qr(index) {
    var xhr = new XMLHttpRequest();
    var objectToSend = {};
    objectToSend["Index"] = index;
    object = JSON.stringify(objectToSend);
    xhr.open('POST', 'print_qr/', true);
    xhr.send(object);
    xhr.onreadystatechange = function(e) {
        if (xhr.readyState === 4) {
            console.log("Edit sent");
        }
    }
}

function toggle_visibility(button) {
    section = button.parentElement.parentElement.getElementsByClassName('section-member')[0];
    section.classList.toggle('hidden');
}