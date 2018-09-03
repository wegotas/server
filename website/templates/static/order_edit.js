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
        console.log(xhr.responseText);
        var infoWindow = window.open('', "", "width=1100,height=650");
        infoWindow.document.body.innerHTML = xhr.responseText;
        location.reload();
      }
      else if (xhr.status == 404) {
        alert('Failed to remove this computer from order');
      }
    }
  }
}