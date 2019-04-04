function deleteDriveFromHddEdit(index) {
	if (confirm('Do you really want to delete this hdd?')) {
		var xhr = new XMLHttpRequest();
		xhr.open('POST', location.href.replace('/hdd_edit/', '/hdd_delete/'), true);
		xhr.send();
		xhr.onreadystatechange = function(e) {
      if (xhr.readyState == 4) {
        if (xhr.status == 200) {
          var infoWindow = window.open(get_main_url() + '/success/',"", "width=620,height=340");
          window.close();
        }
        if (xhr.status == 404) {
          document.getElementsByTagName('body')[0].innerHTML = xhr.responseText;
        }
      }
	}
  }
}

function viewPDFfromDriveEdit(index) {
  var pdfWindow = window.open(location.href.replace('/hdd_edit/', '/view_pdf/'), "", "width=700,height=800");
}

function get_main_url() {
    parts = location.href.split('/');
    parts.pop();
    parts.pop();
    parts.pop();
    return parts.join('/');
}

function open_computer(index) {
    var contentWindow = window.open(get_main_url() + '/edit/' + index + '/', "", "width=400,height=650");
}

function open_lot(index) {
    var contentWindow = window.open(get_main_url() + '/content/' + index + '/', "", "width=1100,height=650");
}

function open_order(index) {
    var contentWindow = window.open(get_main_url() + '/hdd_order_content/' + index + '/', "", "width=1100,height=650");
}