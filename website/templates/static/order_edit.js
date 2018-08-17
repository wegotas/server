var listenerisAdded = false;

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