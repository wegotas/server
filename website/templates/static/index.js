var records_selected = 0;
var filters_selected = 0;

class AFHolder {
  constructor(id_name) {
    this.id_name = id_name;
    this.items = [];
  }

  add(value) {
    this.items.push(value);
  }

  remove(value) {
    var index = this.items.indexOf(value);
    if (index > -1) {
      this.items.splice(index, 1);
    }
  }

  length() {
    return this.items.length;
  }

  debug() {
    console.log(this.id_name);
    console.log(this.items);
  }
}

class AFManager {
  constructor() {
    this.filter_list = []
  }

  add_filter(filter_name, value) {
    var found = false;
    for (var i=0; i<this.filter_list.length; i++) {
      if(this.filter_list[i].id_name == filter_name) {
        found = true;
        this.filter_list[i].add(value);
        break;
      }
    }
    if(!found){
      var filter = new AFHolder(filter_name);
      filter.add(value);
      this.filter_list.push(filter);
    }
    this.debug();
  }

  remove_filter(filter_name, value){
    for (var i=0; i<this.filter_list.length; i++) {
      if(this.filter_list[i].id_name == filter_name) {
        this.filter_list[i].remove(value);
        if(this.filter_list[i].length()==0){
          this.filter_list.splice(i, 1);
        }
        break;
      }
    }
    this.debug();
  }

  debug() {
    for (var i=0; i<this.filter_list.length; i++){
      this.filter_list[i].debug();
    }
    console.log("________________________________________");
  }
}

var afmanager = new AFManager();

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
  parent = checkbox.parentElement;
  // console.log(parent);
  grandparent = parent.parentElement;
  // console.log(grandparent);
  child = grandparent.childNodes[3];
  // console.log(child);
  text = child.innerText;
  // console.log(text);
  grandgrandparent = grandparent.parentElement;
  // console.log(grandgrandparent);
  id = grandgrandparent.id;
  // console.log(id);
  if (checkbox.checked){
      filters_selected++;
      afmanager.add_filter(id, text);
  } else {
      filters_selected--;
      afmanager.remove_filter(id, text);
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

function handleSelect(element) {
  window.location = element.value;
}
