let btn = document.querySelector('#btn');
let sidebar = document.querySelector('.sidebar');
let searchBtn = document.querySelector('.bx-search');

function showIssueModal(name, rate, issue) {
    document.getElementById("modalIssueNameInput").value = name;
    document.getElementById("modalIssueUnitRate").value = rate;
    document.getElementById("modalIssueUnitIssue").value = issue;
    document.querySelector(".issue_modal_container").style.display = "block";
    document.querySelector(".background_wrapper").style.display = "block";
};

function showSupplierModal(name, rate, issue) {
    document.getElementById("modalSupplierNameInput").value = name;
    document.getElementById("modalSupplierUnitRate").value = rate;
    document.getElementById("modalSupplierUnitIssue").value = issue;
    document.querySelector(".supplier_modal_container").style.display = "block";
    document.querySelector(".background_wrapper").style.display = "block";
};

function closeIssueModal() {
    event.preventDefault();
    document.querySelector(".issue_modal_container").style.display = "none";
    document.querySelector(".background_wrapper").style.display = "none";
}

function closeSupplierModal() {
    event.preventDefault();
    document.querySelector(".supplier_modal_container").style.display = "none";
    document.querySelector(".background_wrapper").style.display = "none";
}

function handleNewStock() {
    document.querySelector(".new_stock").style.display = "block";
    document.querySelector(".background_wrapper").style.display = "block";
}

function closeNewStockModal() {
    event.preventDefault();
    document.querySelector(".new_stock").style.display = "none";
    document.querySelector(".background_wrapper").style.display = "none";
}


function showFilterModal() {
    // document.querySelector(".issue_modal_container").style.display = "block";
    document.querySelector(".filter_container").style.display = "block";
};

function closeFilterModal() {
    event.preventDefault();
    document.querySelector(".filter_container").style.display = "none";
    // document.querySelector(".background_wrapper").style.display = "none";
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



btn.onclick = function () {
    sidebar.classList.toggle("active");
}

searchBtn.onclick = function () {
    sidebar.classList.toggle("active");
}


function closeNewStockEditModal() {
    event.preventDefault();
    document.querySelector(".new_stock_edit").style.display = "none";
    document.querySelector(".background_wrapper").style.display = "none";
}

function handleNewStockEditUnit(id, name) {

    const nameInput = document.querySelector('#modalEditNameInput');
    // const packAmountInput = document.querySelector('#inputEditPackAmount');
    // const unitIssueInput = document.querySelector('#inputEditUnitIssue');
    const idInput = document.querySelector('#modalEditIdInput');

    if (!nameInput || !idInput) {
        console.error("One or more input fields not found");
        return;
    }

    document.querySelector(".new_stock_edit").style.display = "block";
    document.querySelector(".background_wrapper").style.display = "block";
    
    
    nameInput.value = name;
    idInput.value = id;
}