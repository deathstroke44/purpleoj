class AddInputsTextArea {
    constructor(mediator, id) {
        this.mediator = mediator;
        this.inputTextArea = document.getElementById(id);
        this.mediator._inputsTextArea = this.inputTextArea;
        this.mediator._inputsTextArea.addEventListener('keyup',function () {
            mediator.inputsChanged();

        });
    }

}