class AddDropdown {
     constructor(mediator, id) {
        this.mediator = mediator;
        this.select = document.getElementById(id);
        this.mediator._dropDown = this.select;
        this.select.addEventListener('change',function () {
            mediator.dropDownSelectAction();
        },false);
    }
}