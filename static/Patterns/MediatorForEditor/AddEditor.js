class AddEditor{
    constructor(mediator,id,config){
        this.mediator = mediator;
        this.editor = CodeMirror.fromTextArea(
                        document.getElementById(id),
                        config);
        this.mediator._editor = this.editor;
        this.editor.on("keyup", function (cm, event) {
            mediator.editorKeyUp(cm, event);
        });

    }

}