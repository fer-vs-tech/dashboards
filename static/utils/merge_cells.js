/*
* Clear the table before merge to avoid wierd behavior
* by removing rowspan and colspan attributes and display: none
*/
function clearTable() {
    // Clear rowspan and colspan attributes of all tables to prevent wierd behavior
    $('.body-content').find('table').each(function () {
        console.log("Cleaning table");
        $(this).find('td[rowspan]').removeAttr('rowspan');
        $(this).find('td[colspan]').removeAttr('colspan');
    });

    // Remove "display: none" from all tables to prevent wierd behavior
    $('.body-content').find('table').each(function () {
        console.log("Removing display: none from table");
        $(this).find('td').each(function () {
            $(this).css('display', '');
        });
    });
}

/*
* This function merges the cells in the table with the same value automatically
* Work vertically from top to bottom and horizontally from left to right
* param tableClass: the class of the table to merge 
*/
function autoMergeDuplicateCells(tableClass) {
    let lenTable = $(tableClass).length;
    console.log('autoMergeDuplicateCells - tables: ' + lenTable);

    if (lenTable > 0) {
        $(tableClass).each(function () {
            $(tableClass).find('td').each(function () {
                let $this = $(this);
                let col = $this.index();
                let html = $this.html();
                let value = $this.text();
                let rowSpan = 1;
                let cell_above = $($this.parent().prev().children()[col]);

                // Look for cells one above another with the same text
                // If the text is the same and the value is not numeric
                while (cell_above.html() === html && isMergableCell(value)) {
                    rowSpan += 1; // Increase the span
                    cell_above_old = cell_above; // Store this cell
                    cell_above = $(cell_above.parent().prev().children()[col]); // and go to the next cell above
                }

                // If there are at least two columns with the same value, 
                // Set a new span to the first and hide the other
                if (rowSpan > 1) {
                    $(cell_above_old).attr('rowspan', rowSpan);
                    $this.hide();
                }

            });

            // Perform colspan row wise
            $(tableClass).find('tr').each((index, tr) => {
                console.log("Start of row");
                // Get first td of the row 
                let td = $(tr).find('td').eq(0);
                // Set default colspan to 1
                let colspan = 1;

                // If td exist then proceed recursively
                while (td.text() !== "" && isMergableCell(td.text())) {
                    // Find next td
                    let next = td.next();
                    // If current td and next td has same text then remove next td
                    if (td.text() == next.text()) {
                        // Remove next td, increase colspan and set it to current td
                        next.remove();
                        colspan += 1;
                        td.attr('colspan', colspan);
                    } else {
                        // Reset colspan to 1 and select next td
                        colspan = 1;
                        td = next;
                    }
                }
            });
        });
    }

}


/*
* Checks if the value is numeric or not
* param value: value to check
* return: true if the value is numeric, false otherwise
*/
function isMergableCell(value) {
    // Remove "%" sign if exists
    if (value.includes('%')) {
        value = value.replace('%', '');
    }

    // Check if the value is numeric, or delimited by a comma, or minus sign
    let result = /^(?:\d{1,3}(?:,\d{3})*$|^\d+$)/.test(value);
    result = result || !isNaN(value) || value.includes('-');
    return !result;
}


/* 
* Get the indexes of the columns that can be merged
* param tableID: the ID of the table to merge
* return: an array of indexes of the columns that can be merged
*/
function getMergableColumnIndexes(tableID) {
    const column_indexes = {
        "dashboard-9-12-5-table": [0],
        "dashboard-9-12-6-table": [0],
        "dashboard-9-12-7-table": [0],
        "dashboard-9-12-8-table": [0],
        "dashboard-9-12-10-table": [0, 1],
        "dashboard-9-12-11-table": [0, 1],
        "dashboard-9-12-12-table": [0, 1],
    }

    return column_indexes[tableID];
}


/*
* Enable or disable the tabs based on the parameter
* param isDisabled: true to disable the tabs, false to enable the tabs
*/
function disableTabs(isDisabled) {
    // Get all the tabs
    let tabs = $('[role="tab"]');

    // Enable or disable the tabs
    tabs.each(function () {
        let $this = $(this);
        // Set the disabled attribute and class name
        $this.attr('aria-disabled', isDisabled);
        if (isDisabled) {
            $this.addClass('disabled');
            $this.css('cursor', 'progress');
            $this.removeAttr('href');
        } else {
            $this.removeClass('disabled');
            $this.css('cursor', 'pointer');
            $this.attr('href', '#');
        }
        // console.log('Tab ' + $this.text() + ' is disabled: ' + isDisabled);
    });
    console.log('Tabs are disabled: ' + isDisabled);
}

// Listen a tag with role button with "tab" and class doesn't contain "active-tab-label" in it
// and perform the merge when the page is loaded and desired table is found
$(document).on('click', '[role="tab"]', function () {
    let $this = $(this);
    // Check if the clicked tab is not active
    if (!$this.hasClass('active-tab-label')) {
        console.log('Tab clicked');

        // Disable the tabs to avoid multiple clicks while the table is loading
        setTimeout(function () {
            disableTabs(true);
        }, 50);

        // Check if the table is loaded every 0.5 seconds for 2 minute
        // untill div class "dash-spinner" is not found then perform the merge
        let interval = setInterval(function () {
            // Check if the table is fully loaded
            if ($('.dash-spinner').length == 0) {
                console.log('Table loaded and ready to merge');
                // Clear the table before merge to avoid wierd behavior
                clearTable();

                // Perform the merge
                autoMergeDuplicateCells('.merged-cell');

                // Stop the interval after merge is performed
                clearInterval(interval);
                console.log('Interval cleared after merge');

                // Enable the tabs
                disableTabs(false);
            }
        }, 500);

        // Stop the interval after 120 seconds if the table is not loaded
        setTimeout(function () {
            console.log("Automatic merge stopped after 120 seconds, clearing interval");
            clearInterval(interval);
            // disableTabs(false);
        }, 120000);
    }
});

function generateLoader(isLoading) {
    // Create a loader element
    const loader = document.createElement('<div style="visibility: visible; position: absolute; top: 0px; height: 100%; width: 100%; display: flex; justify-content: center; align-items: center;"><div class=""><div class="dash-spinner dash-default-spinner"><div class="dash-default-spinner-rect1"></div><div class="dash-default-spinner-rect2"></div><div class="dash-default-spinner-rect3"></div><div class="dash-default-spinner-rect4"></div><div class="dash-default-spinner-rect5"></div></div></div></div>');
    console.log(loader);

    // If the loader is not already present in the page
    if (isLoading) {
        // Add the loader to the page after that element
        $('#dashboard-data').append(loader);
    } else {
        // Remove the loader from the page
        $('.dash-spinner').remove();
    }

}
