index = 1
new_ramstick_index = 1;
new_processor_index = 1;
new_gpu_index = 1;
new_battery_index = 1;


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
    observationSearchBox = document.getElementById("observation-search-box");
    observationSearchBox.addEventListener('keypress', function(event) {
        if (enter_pressed_and_keyword_suitable(event, observationSearchBox.value)) {
            search_observation(observationSearchBox.value);
        }
    })

    ramstick_searchbox = document.getElementById("ramstick_searchbox");
    ramstick_searchbox.addEventListener('keypress', function(event) {
        if (enter_pressed_and_keyword_suitable(event, ramstick_searchbox.value)) {
            search_ramsticks(ramstick_searchbox.value);
        }
    })

    processor_searchbox = document.getElementById("processor_searchbox");
    processor_searchbox.addEventListener('keypress', function(event) {
        if (enter_pressed_and_keyword_suitable(event, processor_searchbox.value)) {
            search_processors(processor_searchbox.value);
        }
    })

    gpu_searchbox = document.getElementById("gpu_searchbox");
    gpu_searchbox.addEventListener('keypress', function(event) {
        if (enter_pressed_and_keyword_suitable(event, gpu_searchbox.value)) {
            search_gpus(gpu_searchbox.value);
        }
    })
}

function search_ramsticks(keyword) {
    ramstick_result_toggler = document.getElementById("ramsticks_result_toggler");
    ramstick_adder = document.getElementById("observation-adder");
    var xhr = new XMLHttpRequest();
    computer_id = 0
    xhr.open('GET', getURLtoWorkWith() + '/ramsticks_to_add/' + computer_id + '/' + urlify(keyword) + '/', true)
    xhr.send();
    xhr.onreadystatechange = function(e) {
        if (request_succesful(xhr)) {
            console.log("search_ramsticks succesful");
        }
    }
}

function search_processors(keyword) {
    ramstick_result_toggler = document.getElementById("ramsticks_result_toggler");
    ramstick_adder = document.getElementById("observation-adder");
    var xhr = new XMLHttpRequest();
    computer_id = 0
    xhr.open('GET', getURLtoWorkWith() + '/processors_to_add/' + computer_id + '/' + urlify(keyword) + '/', true)
    xhr.send();
    xhr.onreadystatechange = function(e) {
        if (request_succesful(xhr)) {
            console.log("search_ramsticks succesful");
        }
    }
}

function search_gpus(keyword) {
    ramstick_result_toggler = document.getElementById("ramsticks_result_toggler");
    ramstick_adder = document.getElementById("observation-adder");
    var xhr = new XMLHttpRequest();
    computer_id = 0
    xhr.open('GET', getURLtoWorkWith() + '/gpus_to_add/' + computer_id + '/' + urlify(keyword) + '/', true)
    xhr.send();
    xhr.onreadystatechange = function(e) {
        if (request_succesful(xhr)) {
            console.log("search_ramsticks succesful");
        }
    }
}

window.onload = function() {load()}

function getURLtoWorkWith() {
    parts = location.href.split('/');
    parts.pop();
    parts.pop();
    return parts.join('/');
}

function enter_pressed_and_keyword_suitable(event, keyword){
    if (event.keyCode === 13) {
        event.preventDefault();
        return keyword_suitable_for_search(keyword);
    }
    return false;
}

function keyword_suitable_for_search(keyword) {
    // checks if keyword is empty
    if (keyword  === '') {
        return false;
    }
    // checks if whole keyword consists only of space characters
    if (keyword.split(' ').join('').length === 0) {
        return false;
    }
    return true
}


function urlify (url) {
    urlToReturn = url.split('#').join('%23');
    return urlToReturn;
}

function search_observation(keyword) {
    observation_result_toggler = document.getElementById("observation_result_toggler");
    observation_adder = document.getElementById("observation-adder");
    var xhr = new XMLHttpRequest();
    computer_id = 0
    xhr.open('GET', getURLtoWorkWith() + '/observations_to_add/' + computer_id + '/' + urlify(keyword) + '/', true)
    xhr.send();
    xhr.onreadystatechange = function(e) {
        if (request_succesful(xhr)) {
            observation_adder.classList.remove("hidden");
            observation_result_toggler.classList.remove('hidden');
            observation_adder.innerHTML = xhr.responseText;
        }
    }
}

function request_succesful(xhr) {
    if (xhr.readyState === 4) {
        if (xhr.status == 200){
            return true;
        }
        return false;
    }
    return false;
}

function toggle_observation_results() {
    document.getElementById("observation-adder").classList.toggle("hidden");
}

function add_observation(button, observation_id) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', getURLtoWorkWith() + '/get_observation/' + observation_id + '/');
    xhr.send();
    holder_of_observations = document.getElementById("holder_of_observations");
    xhr.onreadystatechange = function(e) {
        if (xhr.readyState === 4) {
            if (xhr.status == 200) {
                row = button.parentNode.parentNode;
                table = document.getElementById("observation-search-results");
                row.parentNode.removeChild(row);
                var nodes = new DOMParser().parseFromString(xhr.response.trim(), 'text/html').body.childNodes[0];
                holder_of_observations.appendChild(nodes);
            }
            else {
                alert(xhr.responseText);
            }
        }
    }
}

function remove_observation(button) {
    button.parentNode.parentNode.removeChild(button.parentNode);
}

function new_ramstick(button) {
    holder_of_ramsticks = document.getElementById("holder_of_ramsticks");
    ramstick_holder = create_item_holder()
    ramstick_holder.appendChild(create_ramstick_table());
    holder_of_ramsticks.appendChild(ramstick_holder);
}

function create_ramstick_table() {
    table = document.createElement("table");
    table.classList.add("table");
    table.appendChild(create_row(title_name="Capacity:", name="newramstick_capacity_" + new_ramstick_index, list_name="capacities", values=many_to_many_unique_values["RAMs"]["capacities"]));
    table.appendChild(create_row(title_name="Clock:", name="newramstick_clock_" + new_ramstick_index, list_name="clocks", values=many_to_many_unique_values["RAMs"]["clocks"]));
    table.appendChild(create_row(title_name="Type:", name="newramstick_type_" + new_ramstick_index, list_name="types", values=many_to_many_unique_values["RAMs"]["types"]));
    new_ramstick_index++;
    return table;
}

function new_processor(button) {
    holder_of_processors = document.getElementById("holder_of_processors");
    processor_holder = create_item_holder()
    processor_holder.appendChild(create_processor_table());
    holder_of_processors.appendChild(processor_holder);
}

function create_processor_table() {
    table = document.createElement("table");
    table.classList.add("table");
    table.appendChild(create_row(title_name="Manufacturer:", name="newproc_manufacturername_" + new_processor_index, list_name="manufacturer_names", values=many_to_many_unique_values["Processors"]["manufacturer_names"]));
    table.appendChild(create_row(title_name="Model:", name="newproc_modelname_" + new_processor_index, list_name="model_names", values=many_to_many_unique_values["Processors"]["model_names"]));
    table.appendChild(create_row(title_name="Stock clock:", name="newproc_stockclock_" + new_processor_index, list_name="stock_clocks", values=many_to_many_unique_values["Processors"]["stock_clocks"]));
    table.appendChild(create_row(title_name="Max clock:", name="newproc_maxclock_" + new_processor_index, list_name="max_clocks", values=many_to_many_unique_values["Processors"]["max_clocks"]));
    table.appendChild(create_row(title_name="Core count:", name="newproc_cores_" + new_processor_index, list_name="cores", values=many_to_many_unique_values["Processors"]["cores"], applyNumberFilter=true));
    table.appendChild(create_row(title_name="Thread count:", name="newproc_threads_" + new_processor_index, list_name="threads", values=many_to_many_unique_values["Processors"]["threads"], applyNumberFilter=true));
    new_processor_index++;
    return table;
}

function new_gpu(button) {
    holder_of_gpus = document.getElementById("holder_of_gpus");
    gpus_holder = create_item_holder()
    gpus_holder.appendChild(create_gpu_table());
    holder_of_gpus.appendChild(gpus_holder);
}

function create_gpu_table() {
    table = document.createElement("table");
    table.classList.add("table");
    table.appendChild(create_row(title_name="Manufacturer:", name="newgpu_manufacturername_" + new_gpu_index, list_name="manufacturer_names", values=many_to_many_unique_values["GPUs"]["manufacturer_names"]));
    table.appendChild(create_row(title_name="GPU:", name="newgpu_gpuname_" + new_gpu_index, list_name="gpu_names", values=many_to_many_unique_values["GPUs"]["gpu_names"]));
    new_gpu_index++;
    return table;
}

function create_item_holder() {
    item_holder = document.createElement("div");
    item_holder.classList.add("table-holder");

    close_button = document.createElement("button");
    close_button.type = "button";
    close_button.addEventListener("click", function() {remove_observation(this)});
    close_button.innerHTML = 'x';
    close_button.classList.add("close_button");
    item_holder.appendChild(close_button);
    return item_holder;
}

function create_row(title_name, name, list_name=null, values=null, applyNumberFilter=false) {
    row = document.createElement("tr");
    header = document.createElement("th");
    header.innerHTML = title_name;
    row.appendChild(header);
    cell = document.createElement("td");
    input = document.createElement('input');
    input.type = "text";
    // input.name = name + index;
    input.name = name;
    input.classList.add('input');

    // Adds datalist if list_name and values are provided
    if (list_name!=null && values!=null) {
        datalist = document.createElement('datalist');
        datalist.id = list_name;
        input.setAttribute('list', list_name);
        for (var value of values) {
            option = document.createElement('option');
            option.value = value;
            option.innerHTML = value;
            datalist.appendChild(option);
        }
        cell.appendChild(datalist);
    }

    cell.appendChild(input);
    row.appendChild(cell);

    // adds number filter if applyNumberFilter is true
    if (applyNumberFilter) {
        setInputFilter(input, function(value) { return /^-?\d*$/.test(value); });
    }
    return row;
}