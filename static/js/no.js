function sortNumber() {
    var nomorUrutElems = document.querySelectorAll('.nomor');
    var nomorUrutArray = Array.from(nomorUrutElems);
    nomorUrutArray.sort(function(a, b) {
        return parseInt(a.textContent) - parseInt(b.textContent);
    });
    nomorUrutArray.forEach(function(elem, index) {
        elem.textContent = index + 1;
    });
}
window.addEventListener('load', sortNumber);
