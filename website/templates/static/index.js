var records_selected = 0;
var selected_records = [];
var filters_selected = 0;
var selected_filters = [];

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

  getParameters() {
    var parametersList = [];
    for (var i = 0; i < this.items.length; i++) {
      var parameter = this.id_name + "=" + this.items[i];
      parametersList.push(parameter);
    }
    return parametersList.join("&");
  }

  debug() {
    console.log(this.id_name);
    console.log(this.items);
  }
}

class AFManager {
  constructor() {
    this.filter_list = [];
    this.possible_fieldnames = [];
  }

  process_collection_of_filters(af_div_id) {
    var afSelections = document.getElementById(af_div_id).getElementsByClassName("af-selection");
    for (var i = 0; i<afSelections.length; i++) {
      var afSelection = afSelections[i];
      var title = afSelection.getElementsByClassName("af-chkbxtitle")[0];
      var checkbox = afSelection.getElementsByTagName("input")[0];
      if (checkbox.checked) {
        this.add_filter(afSelection.parentElement.id, title.innerText.trim());
      }
    }
  }

  set_possible_fieldnames() {
    var afDivs = document.getElementsByClassName("autofilter");
    for (var i=0; i<afDivs.length; i++) {
      var fieldname = afDivs[i].getElementsByClassName("af-body")[0];
      this.possible_fieldnames.push(fieldname.id);
    }
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
  }

  remove_filter(filter_name, value) {
    for (var i=0; i<this.filter_list.length; i++) {
      if(this.filter_list[i].id_name == filter_name) {
        this.filter_list[i].remove(value);
        if(this.filter_list[i].length()==0){
          this.filter_list.splice(i, 1);
        }
        break;
      }
    }
  }

  showFilterButton() {
    /*
    console.log("showFilterButton() called");
    */
    var filterButton = document.getElementById("filter");
    /*
    console.log(filterButton);
    */
    if (this.filter_list.length > 0) {
        filterButton.style.display = "inline-block";
    } else {
        filterButton.style.display = "none";
    }
  }

  formNewUrlWithAFURLaddon(url) {
    /*
    console.log(url);
    */
    var splittedArray = url.split("?");
    var mainURL = splittedArray[0];
    var attributesString = splittedArray[1];
    console.log(mainURL);
    console.log(attributesString);
    var attributes = attributesString.split("&");
    console.log(attributes);
    for (var i = attributes.length -1; i > -1; i--) {
      console.log("Attribute: " + attributes[i]);
      for (var j = 0; j < this.possible_fieldnames.length; j++) {
        console.log("Fieldname: " + this.possible_fieldnames[j]);
        if ( attributes[i].includes(this.possible_fieldnames[j])) {
          console.log("Removing");
          attributes.splice(i, 1)
          break;
        }
      }
    }
    console.log(attributes);
    console.log(this.getAFURLaddon());
    return mainURL + "?"+ attributes.join("&") +"&" + this.getAFURLaddon();
  }

  getAFURLaddon() {
    var parametersList = [];
    for (var i = 0; i < this.filter_list.length; i++) {
      parametersList.push(this.filter_list[i].getParameters());
    }
    return parametersList.join("&");
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

window.onload = function() {load_test()}

function load_test() {
  collectSelectedAF();
}

function collectSelectedAF() {
  filterDivs = document.getElementsByClassName("autofilter");
  for (var i = 0; i < filterDivs.length; i++ ){
    afmanager.process_collection_of_filters(filterDivs[i].id);
  }
  afmanager.set_possible_fieldnames();
}

function recordSelect(checkbox){
    if (checkbox.checked){
        selected_records.push(checkbox.value);
    }else {
        selected_records.splice(selected_records.indexOf(checkbox.value), 1);
    }
    if (selected_records.length>0) {
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

function afFilter(checkbox, columnId) {
  columns = document.getElementById(columnId);
}

function afSelect(checkbox) {
  parent = checkbox.parentElement;
  grandparent = parent.parentElement;
  child = grandparent.childNodes[3];
  text = child.innerText;
  grandgrandparent = grandparent.parentElement;
  id = grandgrandparent.id;
  if (checkbox.checked){
      afmanager.add_filter(id, text);
  } else {
      afmanager.remove_filter(id, text);
  }
  afmanager.showFilterButton();
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
  newURL = formationOfURL(element.value);
  loadPage(newURL);
}

function formationOfURL(parameterString) {
  href = location.href;
  string = parameterString.substr(1);
  stringList = string.split('&');
  for (var i =0; i<stringList.length; i++) {
    fieldName = stringList[i].split('=')[0];
    regString = "&" + fieldName + "=[0-9]+"
    pattern = new RegExp(regString, "g");
    href = href.replace(pattern, "");
  }
  return href + parameterString;
}

function loadPage(newURL) {
  window.location = newURL;
}

/*
function search(){
  var parameterArray = [];
  var preExistingParametersArray = [];
  searchKeyword = document.getElementById("search_input").value;
  console.log(searchKeyword);
  parameterArray.push("keyword="+searchKeyword);
  console.log(parameterArray);

  var baseURL, preExistingParameters;
  if (location.href.includes("?")) {
    [baseURL, preExistingParameters] = location.href.split("?");
    preExistingParametersArray = preExistingParameters.split("&");
  }
  else {
    baseURL = location.href;
  }
  console.log(baseURL);
  console.log(preExistingParametersArray);
}
*/

/*
function search() {
  var input, filter, table, tr, td, i;
  console.log("Search called");
  input = document.getElementById("search_input");
  filter = input.value.toUpperCase();
  table = document.getElementById("contents-table");
  trs = table.getElementsByTagName("tr");
  for (i=0; i < trs.length; i++) {
    td = trs[i].getElementsByTagName("td")[2];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
        trs[i].style.display = "";
        console.log("Show");
      }
      else {
        trs[i].style.display = "none";
        console.log("Not show");
      }
    }
  }
}
*/

function search() {
  var input, filter, table, trs, tr, td, i, j, found, indexes;
  indexes = [2,3,4,5,6,7];
  input = document.getElementById("search_input");
  filter = input.value.toUpperCase();
  table = document.getElementById("contents-table");
  trs = table.getElementsByTagName("tr");
  for (i=0; i < trs.length; i++) {
    found = false;
    if (i==0)
    {
      continue;
    }
    for (j=0; j < indexes.length; j++) {
      tr = trs[i];
      tds = tr.getElementsByTagName("td");
      td = tds[indexes[j]];
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
        found = true;
      }
    }
    if (found) {
      trs[i].style.display = "";
    }
    else {
      trs[i].style.display = "none";
    }
  }
}

function mass_delete() {
  if (confirm("Do you really want do delete these records?")) {
    var xhr = new XMLHttpRequest();
    indexArray = JSON.stringify(selected_records);
    xhr.open('POST', 'mass_delete/', true);
    xhr.send(indexArray);
    xhr.onreadystatechange = function(e) {
      if (xhr.readyState === 4) {
        location.reload();
      }
    }
  }
}

function mass_excel() {
  var xhr = new XMLHttpRequest();
  var runAsync = true ;
  indexArray = JSON.stringify(selected_records);
  xhr.open('POST', 'mass_excel/', true);
  xhr.responseType = "arraybuffer";
  xhr.send(indexArray);
  xhr.onreadystatechange = function(e) {
    if (xhr.readyState === 4) {
      console.log(xhr.response);
      const link = document.createElement( 'a' );
      link.style.display = 'none';
      document.body.appendChild( link );

      const blob = new Blob( [ xhr.response ], { type: '‘application/octet-binary' } );
      const objectURL = URL.createObjectURL( blob );

      link.href = objectURL;
      link.href = URL.createObjectURL( blob );
      link.download =  'excel.xlsx';
      link.click();
      }
  }

}

function mass_catchange(element) {
  if (confirm("Do you really want do move these records to another category?")) {
    var xhr = new XMLHttpRequest();
    var objectToSend = {};
    objectToSend[element.value] = selected_records;
    indexArray = JSON.stringify(objectToSend);
    xhr.open('POST', 'cat_change/', true);
    xhr.send(indexArray);
    xhr.onreadystatechange = function(e) {
      if (xhr.readyState === 4) {
        location.reload();
      }
    }
  }
}

function applyAFs() {
  newURL = afmanager.formNewUrlWithAFURLaddon(location.href);
  /*
  console.log(newURL);
  */
  loadPage(newURL);

}

function launchCatWindow() {
    var catWindow = window.open('cat/', "", "width=400,height=650");
}

function launchTypWindow() {
    var typWindow = window.open('typ/', "", "width=400,height=650");
}

function launchTesterWindow() {
    var testerWindow = window.open('test/', "", "width=400,height=650");
}

function launchNewRecordWindow() {
    var testerWindow = window.open('new_record/', "", "width=400,height=650");
}
