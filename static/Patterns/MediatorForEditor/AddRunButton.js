class AddRunButton{
    constructor(mediator, id) {
        this.mediator = mediator;
        this.button = document.getElementById(id)
        this.mediator._runButton = this.button;


    }
}