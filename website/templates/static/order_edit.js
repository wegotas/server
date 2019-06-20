window.onload = function() {load()}

function load() {
    search_textbox = document.getElementById('search_input');
    search_textbox.addEventListener('keyup', function(event) {
        event.preventDefault();
        toggle_search_button();
        search_button = document.getElementById('search_button');
        if (event.keyCode === 13 && !search_button.disabled) {
            search();
        }
    })
}

function toggle_search_button() {
    var search_button = document.getElementById('search_button');
    var search_keyword = document.getElementById("search_input").value;
    if (search_keyword !== '') {
        search_button.disabled = false;
    } else {
        search_button.disabled = true;
    }
    if (search_keyword.split(' ').join('').length === 0) {
        search_button.disabled = true;
    }
}

function edit(index) {
  var editWindow = window.open(window.location.origin+'/website/edit/'+index+'/', "", "width=400,height=650");
}

function disableElements(checkbox) {
	disableFunctions(checkbox);
	disableCheckboxes(checkbox);
	disableSelects(checkbox);
}

function disableFunctions(checkbox) {
	var blockables = document.getElementsByClassName("blockable");
	for (var i=0; i<blockables.length; i++) {
		blockables[i].readOnly = checkbox.checked;
	}
}

function disableCheckboxes(checkbox) {
	var blockableCheckboxes = document.getElementsByClassName("blockableCheckbox");
	for (var i=0; i<blockableCheckboxes.length; i++) {
		blockableCheckboxes[i].readOnly = checkbox.checked;
		if (checkbox.checked) {
			blockableCheckboxes[i].onclick = function()  {uncheck(this, checkbox.checked) };
		} else {
			blockableCheckboxes[i].onclick = null;
		}
	}
}

function uncheck(checkbox) {
	checkbox.checked = !checkbox.checked;
}

function disableSelects(checkbox) {
	var blockableSelects = document.getElementsByClassName("blockableSelect");
	for (var i=0; i<blockableSelects.length; i++) {
		blockableSelects[i].disabled = checkbox.checked;
	}
}

function beforeSubmit() {
	var blockableSelects = document.getElementsByClassName("blockableSelect");
	for (var i=0; i<blockableSelects.length; i++) {
		blockableSelects[i].disabled = false;
	}
}

function remove_from_order(index) {
    if (confirm('Do you really want to remove this computer from this order?')) {
         URLtoWorkWith = location.href;
         parts = URLtoWorkWith.split('/');
         parts.pop();
         parts.pop();
         parts.pop();
         URLtoWorkWith = parts.join('/');
         URLtoWorkWith = URLtoWorkWith + '/strip_order/'+index+'/'
         console.log(URLtoWorkWith);
         var xhr = new XMLHttpRequest();
         xhr.open('POST', URLtoWorkWith);
         xhr.setRequestHeader("Content-type", "application/json");
         xhr.send();
         xhr.onreadystatechange = function() {
            if (xhr.readyState != 4) return;
            if (xhr.status == 200) {
                location.reload();
            } else if (xhr.status == 404) {
                alert('Failed to remove this computer from order');
            }
        }
    }
}

function search() {
    search_text = document.getElementById("search_input").value;
    parts = location.href.split('/');
    parts.pop();
    parts.pop();
    parts.pop();
    URLtoWorkWith = parts.join('/');
    var xhr = new XMLHttpRequest();
    xhr.open('GET', URLtoWorkWith + '/computer_search_table_from_order/?keyword=' + urlify(search_text), true);
    xhr.send();
    document.body.style.cursor = "wait";
    xhr.onreadystatechange = function(e) {
        if (xhr.readyState === 4) {
            search_result_div = document.getElementById('searchResults');
            search_result_div.innerHTML = xhr.responseText;
            search_result_div.classList.remove("hidden");
            document.getElementById("show_hide_search_result").classList.remove("hidden");
        }
        document.body.style.cursor = "default";
    }
}

function toggle_search_result() {
    document.getElementById('searchResults').classList.toggle("hidden");
}

function urlify (url) {
    urlToReturn = url.split('#').join('%23');
    return urlToReturn;
}

function add_to_order(button, computer_id) {
    URLtoWorkWith = location.href + 'add_computer/';
    var xhr = new XMLHttpRequest();
    var objectToSend = {};
    objectToSend["computer_id"] = computer_id;
    json_to_send = JSON.stringify(objectToSend);
    xhr.open('POST', URLtoWorkWith, true);
    xhr.send(json_to_send);
    xhr.onreadystatechange = function(e) {
        if (xhr.readyState === 4) {
            if (xhr.status == 200) {
                button.disabled = true;
                table = document.getElementsByClassName("mainTable")[0];
                var new_row = table.insertRow(-1);
                new_row.innerHTML = xhr.responseText
            }
            else {
                alert(xhr.responseText);
            }
        }
    }
}

function download_excel(url) {
    download_file(url, 'excel.xlsx');
}

function download_csv(url) {
    download_file(url, 'data.csv');
}


function download_file(url, filename) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    xhr.responseType = "arraybuffer";
    xhr.send();
    xhr.onreadystatechange = function(e) {
        if (xhr.readyState === 4) {
            const link = document.createElement( 'a' );
            link.style.display = 'none';
            document.body.appendChild( link );

            const blob = new Blob( [ xhr.response ], { type: '‘application/octet-binary' } );
            const objectURL = URL.createObjectURL( blob );

            link.href = objectURL;
            link.href = URL.createObjectURL( blob );
            link.download = filename;
            link.click();
        }
    }
}
