let btn = document.querySelector('#btn');
let sidebar = document.querySelector('.sidebar');
let searchBtn = document.querySelector('.bx-search');


function handleNewUnit() {
    document.querySelector(".new_unit_container").style.display = "block";
    document.querySelector(".background_wrapper").style.display = "block";
}


function closeEditUnitModal() {
    event.preventDefault();
    document.querySelector(".new_edit_container").style.display = "none";
    document.querySelector(".background_wrapper").style.display = "none";
}

function handleEditUnit(id, name, code) {
    console.log("Function triggered with:", id, name, code);

    const nameInput = document.querySelector('.modalUnitNameInput');
    const codeInput = document.querySelector('.modalUnitCodeInput');
    const idInput = document.querySelector('#modalUnitIdInput');

    if (!nameInput || !codeInput || !idInput) {
        console.error("One or more input fields not found");
        return;
    }

    document.querySelector(".new_edit_container").style.display = "block";
    document.querySelector(".background_wrapper").style.display = "block";
    
    
    nameInput.value = name;
    codeInput.value = code;
    idInput.value = id;
}

function closeEditModal() {
    event.preventDefault();
    document.querySelector(".new_edit_container").style.display = "none";
    document.querySelector(".background_wrapper").style.display = "none";
}

btn.onclick = function () {
    sidebar.classList.toggle("active");
}

searchBtn.onclick = function () {
    sidebar.classList.toggle("active");
}


function handleDeletePopOut(link, name) {
    document.querySelector(".deletePopOut").style.display = "block";
    document.querySelector(".background_wrapper").style.display = "block";
    document.querySelector(".popOutItemLink").href = link;
    document.querySelector(".popOutItemName").innerHTML = name;
}


function closePopOut() {
    event.preventDefault();
    document.querySelector(".deletePopOut").style.display = "none";
    document.querySelector(".background_wrapper").style.display = "none";
}