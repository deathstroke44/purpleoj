class Mediator {

    set editor(value) {
        this._editor = value;

    }

    set checkbox(value) {
        this._checkbox = value;
    }

    set inputsTextArea(value) {
        this._inputsTextArea = value;
    }

    set dropDown(value) {
        this._dropDown = value;
    }


    get editor() {
        return this._editor;
    }

    get checkbox() {
        return this._checkbox;
    }

    get inputsTextArea() {
        return this._inputsTextArea;
    }

    get dropDown() {
        return this._dropDown;
    }


    constructor() {
        this._boilerPlateCodes={};
           this._boilerPlateCodes["Java"]= "class Main {\n" +
            "    public static void main(String[] args) {\n" +
            "        System.out.println(\"Hello, World!\"); \n" +
            "    }\n" +
            "}"
        this._boilerPlateCodes["C"]="#include <stdio.h>\n" +
            "int main()\n" +
            "{\n" +
            "   // printf() displays the string inside quotation\n" +
            "   printf(\"Hello, World!\");\n" +
            "   return 0;\n" +
            "}"
        this._boilerPlateCodes["Python"]="print(\"Hello, World\")"
    }

    setInputTextArea(string){
        this._inputsTextArea.value=string;
    }
    setEditorBoilerPlateCode(string){
        this._editor.getDoc().setValue(string);

    }
    dropDownSelectAction(){
        this.setEditorBoilerPlateCode(this._boilerPlateCodes[this._dropDown.options[this._dropDown.selectedIndex].value]);
        window.alert("Language chosen: "+this._dropDown.options[this._dropDown.selectedIndex].value);
    }


    checkboxAction() {
        if (this._checkbox.checked) {
            document.getElementById('inputs').disabled = false;
            this.setInputTextArea("");


        }
        else {
            this.setInputTextArea("Please check the custom inputs checkbox to enter inputs!!");
            this._inputsTextArea.disabled = true;

        }


    }

    editorKeyUp(cm, event) {
        if (!cm.state.completionActive && /*Enables keyboard navigation in autocomplete list*/
            event.keyCode != 13 && this._editor.getValue().length > 0) {        /*Enter - do not open autocomplete list just after item has been selected in it*/
            CodeMirror.commands.autocomplete(cm, null, {completeSingle: false});

        }
    }
    init(){
        this.setEditorBoilerPlateCode(this._boilerPlateCodes["Python"]);
        this.checkboxAction();


    }

}