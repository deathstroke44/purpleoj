class AddSubmitButton{
    constructor(mediator, id) {
        this.mediator = mediator;
        this.button = document.getElementById(id)
        this.mediator._submitButton = this.button;


    }
}