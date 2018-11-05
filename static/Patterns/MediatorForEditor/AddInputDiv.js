class AddInputDiv {
    constructor(mediator, id) {
        this.mediator = mediator;
        this.inputDiv= document.getElementById(id);
        this.mediator._inputDiv= this.inputDiv;

    }

}