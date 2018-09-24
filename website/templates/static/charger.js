function toggleDetails() {
    var button = document.getElementById("detail-button");
    var details = document.getElementsByClassName('detail');
    if (button.innerHTML.includes("Show")) {
        button.innerHTML = "&nbsp;&#8639; Hide details &#8639;&nbsp;";
        display = "table-row";
    } else {
        button.innerHTML = "&nbsp;&#8643; Show more details &#8642;&nbsp;";
        display = 'none';
    }
    for (detail of details) {
        detail.style.display = display;
    }
}