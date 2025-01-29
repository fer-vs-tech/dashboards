/*
* This is helper code for the upload_wvr.html page
* It handles the logic for the file selection and the folder selection
*/
function handleFolderSelection(event) {
    const files = event.target.files;
    const filteredFiles = [...files].filter(file => file.name.endsWith(".wvr"));
    const wvrPath = filteredFiles[0]?.webkitRelativePath;
    return wvrPath;
}


/*
 * Handle the container size when a folder is selected
 * This is a temporary solution until we have a better UI
*/
function handleContainerSize(controllersContainerHeight = 684, selectContainerHeight = 592) {
    const controllersContainer = document.querySelector('.controllers-container');
    const selectContainer = document.querySelector('.select-menu');
    const filesColumn = document.querySelectorAll('.path');
    // Remove "hide" class from files column
    filesColumn.forEach((column) => {
        column.classList.remove('hide');
    });

    const filesColumnWidth = filesColumn[0]?.offsetWidth;
    const customWidth = filesColumnWidth + 548;
    if (selectContainer !== null) {
        controllersContainer.style.width = customWidth + 'px';
        selectContainer.style.width = customWidth - 93 + 'px';
    } else {
        controllersContainer.style.width = customWidth - 93 + 'px';
    }
}

/*
* Validate the form when a folder is selected
* Disable the submit button if any of the 'select-file' elements is empty
* or no folder is selected yet
*/
function validateForm() {
    // Count the number of 'select-file' elements
    const selectFileElements = document.querySelectorAll('.selected-file');
    // Retrive 'id' attribute and 'value' of each element
    const fileIds = [...selectFileElements].map((element) => {
        const id = element.attributes.id?.value;
        const value = element.innerHTML;
        return { id, value };
    });

    // Check if all the 'select-file' elements have a value
    const isValid = fileIds.every((fileId) => fileId.value !== undefined && fileId.value !== '' && fileId.value !== 'WVR file not found');
    return disableSubmitButton(!isValid)
}


// Toggle the submit button state (disabled or not) based on the 'disable' parameter
function disableSubmitButton(disable) {
    const button = document.querySelector('.button-submit');
    button.disabled = disable;
}


// Select all the select menus and apply the selectmenu jquery plugin
const selectMenus = document.querySelectorAll('select');
selectMenus.forEach((selectMenu) => {
    const name = selectMenu.attributes.name?.value;
    $(`[name="${name}"]`).selectmenu({
        ...selectDefaultOption,
        open: function () {
            handleSelectmenuArrow(this).default();
        },
        close: function () {
            handleSelectmenuArrow(this).rotate();
        },
    });
});


// Adjust container size when a selectmenu element exists
const selectmenuElements = document.querySelectorAll('.wvr-select');
if (selectmenuElements.length > 0) {
    handleContainerSize(542, 449);
}


const fileSelectButtons = document.querySelectorAll('.folder-select')
const popupMenu = document.querySelector('.popup-menu');
const popupItems = document.querySelectorAll('.popup-item');

// Disable the submit button if no folder is selected yet (default state)
if (fileSelectButtons.length > 0) {
    disableSubmitButton(true);
}

// Attach click event to each folder select menu and open the popup menu when clicked on a folder select menu
fileSelectButtons.forEach(item => {
    item.addEventListener('click', e => {
        e.stopPropagation();
        const forAttribute = item.attributes.for?.value;
        popupMenu.setAttribute('data-for', forAttribute);
        popupMenu.classList.remove('hidden');
    });
});

// Attach click event to each popup item and close the popup menu when clicked on an item
popupItems.forEach(item => {
    item.addEventListener('click', e => {
        e.stopPropagation();
        popupMenu.classList.add('hidden');

        // Extract the innerHTML from the clicked item
        // assign it to the 'value' attribute of the hidden input
        const result = item.innerHTML;
        const uniqueID = popupMenu.attributes['data-for']?.value;
        const filePath = document.querySelector(`#${uniqueID}_path`);
        const fileName = document.querySelector(`#${uniqueID}_file`);
        if (result) {
            filePath.value = result;
            fileName.innerHTML = result;
        } else {
            filePath.value = '';
            fileName.innerHTML = "WVR file not found";
        }

        // Adjust container size when a folder is selected
        // and validate the form
        handleContainerSize();
        validateForm();
    });
});

// Close the popup menu when clicking outside of it
document.addEventListener('click', e => {
    if (popupMenu !== null && !popupMenu.contains(e.target)) {
        popupMenu.classList.add('hidden');
    }
});
