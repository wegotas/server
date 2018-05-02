var records_selected = 0;
var filters_selected = 0;

function manButPress() {
    var button = document.getElementById("manual-filter-button");
    if (button.innerHTML.includes("Show")){
        button.innerHTML = "&#8639; Hide manual filters &#8638;";
        document.getElementById("manual-filters").style.display = "inline-block";
    } else {
        button.innerHTML = "&nbsp;&#8643; Show manual filters &#8642;&nbsp;";
        document.getElementById("manual-filters").style.display = "none";
    }
}

function recordSelect(checkbox){
    if (checkbox.checked){
        records_selected++;
    }else {
        records_selected--;
    }
    if (records_selected>0) {
        document.getElementById("mass-select-options").style.display = "inline-block";
    } else {
        document.getElementById("mass-select-options").style.display = "none";
    }
}

function recordSelectAll(checkbox){
    /*
    console.log(checkbox.checked)
    checkbox1 = document.getElementById("check1");
    if (checkbox1.checked != checkbox.checked) {
        checkbox1.click();
    }
    checkbox2 = document.getElementById("check2");
    if (checkbox2.checked != checkbox.checked) {
        checkbox2.click();
    }
    */
    workingDiv = document.getElementById("records");
    recordCheckboxes = workingDiv.getElementsByClassName("record-chkbx");
    for (var i =0; i < recordCheckboxes.length; i++) {
      if (recordCheckboxes[i].checked != checkbox.checked)
        recordCheckboxes[i].click();
    }
}

function edit(index) {
    var editWindow = window.open('edit/'+index+'/', "", "width=400,height=650");
}

function autoFilterMenu(filterDivId){
    filterDiv = document.getElementById(filterDivId);
    filterDiv.classList.toggle("show");
}

function afSelect(checkbox) {
  if (checkbox.checked){
      filters_selected++;
  } else {
      filters_selected--;
  }
  if (filters_selected>0) {
      document.getElementById("filter").style.display = "inline-block";
  } else {
      document.getElementById("filter").style.display = "none";
  }
}

function afSelectAll(checkbox ,filterDivId) {
  filterDiv = document.getElementById(filterDivId);
  filterCheckboxes = filterDiv.getElementsByTagName("input");
  for (var i =0; i < filterCheckboxes.length; i++) {
    if (filterCheckboxes[i].checked != checkbox.checked)
      filterCheckboxes[i].click();
  }
}

function filterKeywordChange(inputbox, workingDivId) {
  keyword = inputbox.value;
  workingDiv = document.getElementById(workingDivId);
  selectionDivs = workingDiv.getElementsByClassName("af-selection");
  for (var i =0; i<selectionDivs.length; i++) {
    selectionDiv = selectionDivs[i];
    divs = selectionDiv.childNodes;
    chkbxTitleDiv = selectionDiv.childNodes[3];
    chkbxTitle = chkbxTitleDiv.innerText;
    if (chkbxTitle.includes(keyword)) {
      selectionDivs[i].style.display = "block";
    } else {
      selectionDivs[i].style.display = "none";
    }
  }
}
