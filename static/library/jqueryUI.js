const selectDefaultOption = {
    position: {
        my: 'left top+4',
    },
    icons: {
        button: 'custom-button',
    },
};

const CLASSNAME = {
    SELECTMENU: {
        BUTTON: 'ui-selectmenu-button',
        TEXT: 'ui-selectmenu-text',
        MENU: 'ui-selectmenu-menu',
        MENU_WRAPPER: 'ui-menu',
        MENU_ITEM: 'ui-menu-item',
        MENU_ITEM_WRAPPER: 'ui-menu-item-wrapper',
    },
};

function handleSelectmenuArrow(selectElement) {
    const arrowElement = $(selectElement).siblings('.arrow');
    return {
        default: function () {
            if (!arrowElement.hasClass('rotate')) arrowElement.addClass('rotate');
        },
        rotate: function () {
            if (arrowElement.hasClass('rotate')) arrowElement.removeClass('rotate');
        },
    };
}

function handleAutocompleteArrow(autocompleteElement) {
    const arrowElement = $(autocompleteElement).siblings('.arrow');
    return {
        show: function () {
            if (!arrowElement.hasClass('show')) arrowElement.addClass('show');
        },
        hide: function () {
            if (arrowElement.hasClass('show')) arrowElement.removeClass('show');
        },
        default: function () {
            if (!arrowElement.hasClass('rotate')) arrowElement.addClass('rotate');
        },
        rotate: function () {
            if (arrowElement.hasClass('rotate')) arrowElement.removeClass('rotate');
        },
    };
}
