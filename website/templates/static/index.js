var records_selected = 0;
var selected_records = [];
var filters_selected = 0;
var selected_filters = [];


class Holder {
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
}

class SearchOptions {
    constructor() {
        this.options_list = [];
    }

    set_option_row_count() {
        this.option_row_count = document.getElementsByClassName("option-row").length;
    }

    addOption(tagname, text) {
        var found = false;
        for (var i=0; i<this.options_list.length; i++) {
            if(this.options_list[i].id_name == tagname) {
                found = true;
                this.options_list[i].add(text);
                break;
            }
        }
        if(!found){
            var option = new Holder(tagname);
            option.add(text);
            this.options_list.push(option);
        }
        this.toggle_search_button();
    }

    removeOption(tagname, text) {
        for (var i=0; i<this.options_list.length; i++) {
            if(this.options_list[i].id_name == tagname) {
                this.options_list[i].remove(text);
                if(this.options_list[i].length()==0){
                    this.options_list.splice(i, 1);
                }
                break;
            }
        }
        this.toggle_search_button();
    }

    toggle_search_button() {
        var search_button = document.getElementById('search_button');
        var searchKeyword = document.getElementById("search_input").value;
        if (this.options_list.length >= this.option_row_count && searchKeyword !== '' ){
            search_button.disabled = false;
        } else {
            search_button.disabled = true;
        }
        if (searchKeyword.split(' ').join('').length === 0) {
            search_button.disabled = true;
        }
    }

    getOptionsAddon() {
        var parametersList = [];
        for (var i = 0; i < this.options_list.length; i++) {
            parametersList.push(this.options_list[i].getParameters());
        }
        var stringToReturn = parametersList.join("&");
        if (stringToReturn != "") {
            stringToReturn = "&" + stringToReturn;
        }
        return stringToReturn;
    }

    process_option(checkbox) {
        var tagname = checkbox.name;
        var text = checkbox.parentElement.getElementsByClassName("option-fieldname")[0].innerText;
        if (checkbox.checked) {
            this.addOption(tagname, text);
        } else {
            this.removeOption(tagname, text);
        }
    }

    callect_initial_options() {
        var checkboxes = document.getElementsByClassName("option-checkbox");
        for (checkbox of checkboxes) {
            this.process_option(checkbox);
        }
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
      var filter = new Holder(filter_name);
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
    var filterButton = document.getElementById("filter");
    if (this.filter_list.length > 0) {
        filterButton.style.display = "inline-block";
    } else {
        filterButton.style.display = "none";
    }
  }

  formNewUrlWithAFURLaddon(url) {
    var splittedArray = url.split("?");
    var mainURL = splittedArray[0];
    var attributesString = splittedArray[1];
    if (attributesString == null) {
    	return mainURL + '?' + this.getAFURLaddon();
    }
    else {
	    var attributes = attributesString.split("&");
	    if (this.filter_list.length === 0){
	        for (var i = attributes.length -1; i > -1; i--) {
                for (var j = 0; j < this.possible_fieldnames.length; j++) {
                    if ( attributes[i].includes(this.possible_fieldnames[j])) {
                        attributes.splice(i, 1);
                        break;
                    }
                }
            }
	    }

	    /*This part removes empty strings from the array*/
	    for (var i=attributes.length-1; i >= 0; i--) {
            if (attributes[i] === "") {
                attributes.splice(i, 1);
            }
        }
        console.log(attributes);
	    return mainURL + "?"+ attributes.join("&")  + this.getAFURLaddon();
    }
  }

  getAFURLaddon() {
    var parametersList = [];
    for (var i = 0; i < this.filter_list.length; i++) {
      parametersList.push(this.filter_list[i].getParameters());
    }
    var stringToReturn = parametersList.join("&");
    if (stringToReturn != "") {
        stringToReturn = "&" + stringToReturn;
    }
    return stringToReturn;
  }
}

var afmanager = new AFManager();
var searchoptions = new SearchOptions();

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

window.onload = function() {load()}

function load() {
    collectSelectedAF();
    lockStatuses();
    search_textbox = document.getElementById('search_input');
    search_textbox.addEventListener('keyup', function(event) {
        event.preventDefault();
        searchoptions.toggle_search_button();
        search_button = document.getElementById('search_button');
        if (event.keyCode === 13 && !search_button.disabled) {
            search_using_keyword();
        }
    })
    searchoptions.set_option_row_count();
    searchoptions.callect_initial_options();
}

function remove_keyword() {
  href = location.href;
  regChecker = /[&|?]keyword=[A-Za-z0-9]+/;
  if (regChecker.test(href)){
    regString = "[&|?]keyword=[A-Za-z0-9]+";
    pattern = new RegExp(regString, "g");
    return href.replace(pattern, "")
  }
  return location.href;
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

function edit_computer(url) {
    var editWindow = window.open(url, "", "width=400,height=650");
}

function deleteOrder(url) {
    if (confirm("Do you really want to delete this order?")) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', url, true);
        xhr.send();
        xhr.onreadystatechange = function(e) {
            if (xhr.readyState === 4) {
                console.log(xhr.status);
                if (xhr.status == 200) {
                    location.reload();
                }
                else {
                    var infoWindow = window.open('', '', "width=1000,height=650");
                    infoWindow.document.body.innerHTML = xhr.responseText;
                }
            }
        }
    }
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
}

function afSelectAll(checkbox ,filterDivId) {
    filterDiv = document.getElementById(filterDivId);
    filterCheckboxes = filterDiv.getElementsByTagName("input");
    for (var i =0; i < filterCheckboxes.length; i++) {
        style = filterCheckboxes[i].parentElement.parentElement.style.display
        if (filterCheckboxes[i].checked != checkbox.checked && style !== "none")
            filterCheckboxes[i].click();
    }
}

function filterKeywordChange(inputbox, workingDivId) {
    keyword = inputbox.value.toUpperCase();
    workingDiv = document.getElementById(workingDivId);
    selectionDivs = workingDiv.getElementsByClassName("af-selection");
    for (var i =0; i<selectionDivs.length; i++) {
        selectionDiv = selectionDivs[i];
        divs = selectionDiv.childNodes;
        chkbxTitleDiv = selectionDiv.childNodes[3];
        chkbxTitle = chkbxTitleDiv.innerText.toUpperCase();
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
        regString = "&?" + fieldName + "=[0-9]+"
        pattern = new RegExp(regString, "g");
        href = href.replace(pattern, "");
    }
    result = href + parameterString;
    if (!href.includes('?')) {
        result = result.replace('&', '?');
    }
    if (href.includes('?&')) {
        result = result.replace('?&', '?');
    }
    return result
}

function loadPage(newURL) {
    window.location = newURL;
}

function toggle_category_choices() {
    categoryChoices = document.getElementsByClassName("search-categories")[0];
    categoryChoices.classList.toggle("show");
}

function search_using_keyword() {
    variable1 = document.getElementById("search_input");
    variable2 = variable1.value;
    searchKeyword = document.getElementById("search_input").value;
    searchAddon = searchoptions.getOptionsAddon();
    URLtoWorkWith = location.href.split('?')[0]
    href = remove_keyword();
    location.href = '/website/search/?keyword=' + urlify(searchKeyword) + urlify(searchAddon)
}

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

function mass_delete(url) {
    if (confirm("Do you really want do delete these records?")) {
        var xhr = new XMLHttpRequest();
        indexArray = JSON.stringify(selected_records);
        xhr.open('POST', url, true);
        xhr.send(indexArray);
        xhr.onreadystatechange = function(e) {
            if (xhr.readyState === 4) {
                location.reload();
            }
        }
    }
}

function mass_excel(url) {
    var xhr = new XMLHttpRequest();
    var runAsync = true ;
    indexArray = JSON.stringify(selected_records);
    xhr.open('POST', url, true);
    xhr.responseType = "arraybuffer";
    xhr.send(indexArray);
    xhr.onreadystatechange = function(e) {
        if (xhr.readyState === 4) {
            const link = document.createElement( 'a' );
            link.style.display = 'none';
            document.body.appendChild( link );

            const blob = new Blob( [ xhr.response ], { type: '‘application/octet-binary' } );
            const objectURL = URL.createObjectURL( blob );

            link.href = objectURL;
            link.href = URL.createObjectURL( blob );
            link.download = 'excel.xlsx';
            link.click();
        }
    }
}

function mass_csv(url) {
    var xhr = new XMLHttpRequest();
    var runAsync = true ;
    indexArray = JSON.stringify(selected_records);
    xhr.open('POST', url, true);
    xhr.responseType = "arraybuffer";
    xhr.send(indexArray);
    xhr.onreadystatechange = function(e) {
        if (xhr.readyState === 4) {
            const link = document.createElement( 'a' );
            link.style.display = 'none';
            document.body.appendChild( link );

            const blob = new Blob( [ xhr.response ], { type: '‘application/octet-binary' } );
            const objectURL = URL.createObjectURL( blob );

            link.href = objectURL;
            link.href = URL.createObjectURL( blob );
            link.download = 'data.csv';
            link.click();
        }
    }
}

function mass_qr_print() {
    var xhr = new XMLHttpRequest();
    var runAsync = true ;
    indexArray = JSON.stringify(selected_records);
    xhr.open('POST', '/website/mass_qr_print/', true);
    /*
    * Incomplete, should be finished, to be able to choose from which printer to print.
    * And printing should be working properly, one row with dt4x, two rows with g500.
    */
    /*
    if (confirm("Do you want to print in the office?")) {
        xhr.open('POST', 'mass_qr_print/Godex_DT4x/', true);
    }
    else {
        xhr.open('POST', 'mass_qr_print/Godex_g500/', true);
    }
    */
    xhr.responseType = "arraybuffer";
    xhr.send(indexArray);
}

function mass_qr_print_with_printer(printer) {
    var xhr = new XMLHttpRequest();
    var runAsync = true ;
    indexArray = JSON.stringify(selected_records);
    xhr.open('POST', '/website/mass_qr_print/' + printer + '/', true);
    /*
    * Incomplete, should be finished, to be able to choose from which printer to print.
    * And printing should be working properly, one row with dt4x, two rows with g500.
    */
    /*
    if (confirm("Do you want to print in the office?")) {
        xhr.open('POST', 'mass_qr_print/Godex_DT4x/', true);
    }
    else {
        xhr.open('POST', 'mass_qr_print/Godex_g500/', true);
    }
    */
    xhr.responseType = "arraybuffer";
    xhr.send(indexArray);
}

function modaljs(id, closeable) {
    var body = document.querySelector("body");
    var parent = document.querySelector(id);
    parent.classList.toggle('on');
    var bg = document.createElement("div");
    var close = document.createElement("div");
    bg.className = "modal-js-overlay";
    close.className = "modal-js-close";

    godex_dt4x_printer_button = create_printer_button("Print in office (Godex_DT4x)");
    godex_g500_printer_button = create_printer_button("Print in warehouse (Godex_G500)");

    if (closeable) {
        close.innerHTML = "x";
        close.addEventListener('click', function () {
            modaljs_window_cleanup(body, parent, godex_dt4x_printer_button, godex_g500_printer_button);
        });
        parent.appendChild(close);
    }
    body.appendChild(bg);

    godex_dt4x_printer_button.addEventListener('click', function () {
        mass_qr_print_with_printer("Godex_DT4x");
        modaljs_window_cleanup(body, parent, godex_dt4x_printer_button, godex_g500_printer_button);
    });
    parent.appendChild(godex_dt4x_printer_button);

    godex_g500_printer_button.addEventListener('click', function () {
        mass_qr_print_with_printer("Godex_G500");
        modaljs_window_cleanup(body, parent, godex_dt4x_printer_button, godex_g500_printer_button);
    });
    parent.appendChild(godex_g500_printer_button);
}

function create_printer_button(title) {
    var button = document.createElement("button");
    button.innerHTML = title;
    button.type = "button";
    button.display = "block";
    return button
}

function modaljs_window_cleanup(body, parent, godex_dt4x_printer_button, godex_g500_printer_button) {
    var overlay = body.querySelector(".modal-js-overlay");
    var closebtn = parent.querySelector(".modal-js-close");
    body.removeChild(overlay);
    parent.classList.toggle('on');
    parent.removeChild(closebtn);
    parent.removeChild(godex_dt4x_printer_button);
    parent.removeChild(godex_g500_printer_button);
}

function mass_catchange(element, url) {
    if (confirm("Do you really want do move these records to another category?")) {
        var xhr = new XMLHttpRequest();
        var objectToSend = {};
        objectToSend[element.value] = selected_records;
        indexArray = JSON.stringify(objectToSend);
        xhr.open('POST', url, true);
        xhr.send(indexArray);
        xhr.onreadystatechange = function(e) {
            if (xhr.readyState === 4) {
                location.reload();
            }
        }
    }
}

function ord_assign(element, url) {
    if (confirm("Do you really want to assign these records to this order?")) {
        var xhr = new XMLHttpRequest();
        var objectToSend = {};
        objectToSend[element.value] = selected_records;
        indexArray = JSON.stringify(objectToSend);
        xhr.open('POST', url, true);
        xhr.send(indexArray);
        xhr.onreadystatechange = function(e) {
            if (xhr.readyState === 4) {
                location.reload();
            }
        }
    }
}

function urlify (url) {
    urlToReturn = url.split('#').join('%23');
    return urlToReturn;
}

function applyAFs() {
    newURL = afmanager.formNewUrlWithAFURLaddon(location.href);
    loadPage(urlify(newURL));
}

function launchWindow(url, dimensions) {
    var newWindow = window.open(url, "", dimensions);
}

function getCatSoldParams() {
    stringArray = [];
    for (var i = 0; i<selected_records.length; i++) {
        stringArray.push("id="+selected_records[i]);
    }
    return "?" + stringArray.join('&');
}

function editDrive(url) {
	var editHddWindow = window.open(url, "", "width=620,height=340");
}

function deleteDrive(url) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', url);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.send();
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return;
        if (xhr.status == 200) {
            var infoWindow = window.open('/website/success/',"", "width=620,height=340");
            setTimeout(location.reload(), 1000);
        }
        else if (xhr.status == 404) {
            alert(xhr.responseText);
        }
    }
}

function viewPdf(url) {
    var pdfWindow = window.open(url, "", "width=700,height=800");
}

function drive_delete_order(url) {
    var contentWindow = window.open(url, "", "width=1100,height=650");
    setTimeout(function(){ location.reload(); }, 1500);
}

function hddOrderOtherCheck(checkbox) {
    statusSelection = document.getElementById('status_selection');
    statusSelection.disabled = checkbox.checked;
    otherSelection = document.getElementById('other_selection');
    otherSelection.disabled = !(checkbox.checked);
}

function lockStatuses() {
    checkbox = document.getElementById('other_checkbox');
    if (checkbox) {
        hddOrderOtherCheck(checkbox);
    }
}

function edit_charger(url) {
    var editChargerWindow = window.open(url, "", "width=700,height=620");
}

function delete_charger(url) {
    if (confirm('Do you really want to delete this charger?')) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', url);
        xhr.setRequestHeader("Content-type", "application/json");
        xhr.send();
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4) {
                if (xhr.status == 200) {
                    var infoWindow = window.open('/website/success/',"", "width=620,height=340");
                    setTimeout(location.reload(), 1000);
                }
                if (xhr.status == 404) {
                    alert(xhr.responseText);
                }
            }
        }
    }
}

function download_hdd_order_csv(index) {
    var xhr = new XMLHttpRequest();
    var runAsync = true ;
    xhr.open('GET', 'csv/', true);
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
            link.download = 'hdd_order.csv';
            link.click();
        }
    }
}

function process_option(checkbox) {
    searchoptions.process_option(checkbox);
}

function open_tar_order_import_window(url){
    var new_window = window.open(url, "", "width=380,height=100");
}

function content(url) {
    var contentWindow = window.open(url, "", "width=1100,height=650");
}

function mass_sold(url) {
    var testerWindow = window.open(url + getCatSoldParams(), "", "width=920,height=600");
}
