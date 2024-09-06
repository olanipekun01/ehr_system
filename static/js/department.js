let btn = document.querySelector('#btn');
let sidebar = document.querySelector('.sidebar');
let searchBtn = document.querySelector('.bx-search');


function handleNewDept() {
    document.querySelector(".new_dept_container").style.display = "block";
    document.querySelector(".background_wrapper").style.display = "block";
}


function closeDeptModal() {
    event.preventDefault();
    document.querySelector(".new_dept_container").style.display = "none";
    document.querySelector(".background_wrapper").style.display = "none";
}




btn.onclick = function () {
    sidebar.classList.toggle("active");
}

searchBtn.onclick = function () {
    sidebar.classList.toggle("active");
}