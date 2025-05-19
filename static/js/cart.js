let btn = document.querySelector('#btn');
let sidebar = document.querySelector('.sidebar');
let searchBtn = document.querySelector('.bx-search');




function openConfirmOrderModal() {
    document.querySelector(".confirm_order").style.display = "block";
    document.querySelector(".background_wrapper").style.display = "block";

    userType = document.querySelector("#checkUserType").value;
    checkMatStaffNo = document.querySelector("#checkMatStaffNo").value;
    fileNo = document.querySelector("#fileNo").value;
    checkFullName = document.querySelector("#checkFullName").value;
    checkDept = document.querySelector("#checkDept").value;


    document.querySelector("#userTypeValue").innerHTML = userType;
    document.querySelector("#nameValue").innerHTML = checkFullName;
    document.querySelector("#matStaffNoValue").innerHTML = checkMatStaffNo;
    document.querySelector("#fileNoValue").innerHTML = fileNo;
    document.querySelector("#deptValue").innerHTML = checkDept;

    document.querySelector("#inputUserType").value = userType;
    document.querySelector("#inputFullName").value = checkFullName;
    document.querySelector("#inputMatStaffNo").value = checkMatStaffNo;
    document.querySelector("#inputFileNo").value = fileNo;
    document.querySelector("#inputDept").value = checkDept;
}

function closeConfirmOrderModal() {
    event.preventDefault();
    document.querySelector(".confirm_order").style.display = "none";
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