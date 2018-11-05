class AddCheckbox {

    constructor(mediator, id) {
        this.mediator = mediator;
        this.checkbox = document.querySelector("input[name=" + id + "]");
        this.mediator.checkbox = this.checkbox;
        this.checkbox.addEventListener('change',function () {
            mediator.checkboxAction();
        });
    }


}