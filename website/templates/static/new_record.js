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
    toggler_variable_pair = {
        "ramsticks_result_toggler":"ramstick-adder" ,
        "processors_result_toggler": "processor-adder",
        "gpus_result_toggler": "gpu-adder",
        "observation_result_toggler": "observation-adder"
    }

    Object.entries(toggler_variable_pair).forEach(entry => {
        let toggler = entry[0];
        let adder = entry[1];
        document.getElementById(toggler).onclick = function(event) {
            document.getElementById(adder).classList.toggle("hidden");
        }
    });

    setInputFilter(document.getElementById("intTextBox"), function(value) { return /^-?\d*$/.test(value); });
    observationSearchBox = document.getElementById("observation-search-box");
    observationSearchBox.addEventListener('keypress', function(event) {
        if (enter_pressed_and_keyword_suitable(event, observationSearchBox.value)) {
            search_item(observationSearchBox.value, "observation_result_toggler", "observation-adder", "observations_to_add");
        }
    })

    ramstick_searchbox = document.getElementById("ramstick_searchbox");
    ramstick_searchbox.addEventListener('keypress', function(event) {
        if (enter_pressed_and_keyword_suitable(event, ramstick_searchbox.value)) {
            search_item(ramstick_searchbox.value, "ramsticks_result_toggler", "ramstick-adder", "ramsticks_to_add");
        }
    })

    processor_searchbox = document.getElementById("processor_searchbox");
    processor_searchbox.addEventListener('keypress', function(event) {
        if (enter_pressed_and_keyword_suitable(event, processor_searchbox.value)) {
            search_item(processor_searchbox.value, "processors_result_toggler", "processor-adder", "processors_to_add");
        }
    })

    gpu_searchbox = document.getElementById("gpu_searchbox");
    gpu_searchbox.addEventListener('keypress', function(event) {
        if (enter_pressed_and_keyword_suitable(event, gpu_searchbox.value)) {
            search_item(gpu_searchbox.value, "gpus_result_toggler", "gpu-adder", "gpus_to_add");
        }
    })
}

function search_item(keyword, item_result_toggler_idname, item_adder_idname, urlpart) {
    item_result_toggler = document.getElementById(item_result_toggler_idname);
    item_adder = document.getElementById(item_adder_idname);
    var xhr = new XMLHttpRequest();
    computer_id = 0
    xhr.open('GET', getURLtoWorkWith() + '/' + urlpart +'/' + computer_id + '/' + urlify(keyword) + '/', true)
    xhr.send();
    xhr.onreadystatechange = function(e) {
        if (request_succesful(xhr)) {
            item_adder.classList.remove("hidden");
            item_result_toggler.classList.remove('hidden');
            item_adder.innerHTML = xhr.responseText;
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

function request_succesful(xhr) {
    if (xhr.readyState === 4) {
        if (xhr.status == 200) {
            return true;
        }
        return false;
    }
    return false;
}

function add_item(button, item_id, urlpart, holder_item_idname, item_search_results_idname) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', getURLtoWorkWith() + '/' + urlpart + '/' + item_id + '/');
    xhr.send();
    holder_of_observations = document.getElementById(holder_item_idname);
    xhr.onreadystatechange = function(e) {
        if (xhr.readyState === 4) {
            if (xhr.status == 200) {
                row = button.parentNode.parentNode;
                table = document.getElementById(item_search_results_idname);
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

function add_observation(button, observation_id) {
    add_item(button, observation_id, "get_observation", "holder_of_observations", "observation-search-results");
}

function add_ramstick(button, ramstick_id) {
    add_item(button, ramstick_id, "get_ramstick", "holder_of_ramsticks", "ram-search-results");
}

function add_processor(button, id_processor) {
    add_item(button, id_processor, "get_processor", "holder_of_processors", "processor-search-results");
}

function add_gpu(button, id_gpu) {
    add_item(button, id_gpu, "get_gpu", "holder_of_gpus", "processor-search-results");
}

function remove_item(button) {
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
    close_button.addEventListener("click", function() {remove_item(this)});
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