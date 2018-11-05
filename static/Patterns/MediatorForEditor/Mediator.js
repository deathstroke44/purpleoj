class Mediator {
    get runButton() {
        return this._runButton;
    }

    set runButton(value) {
        this._runButton = value;
    }

    get submitButton() {
        return this._submitButton;
    }


    get themeSelect() {
        return this._themeSelect;
    }

    set themeSelect(value) {
        this._themeSelect = value;
    }

    set submitButton(value) {
        this._submitButton = value;
    }


    set editor(value) {
        this._editor = value;

    }

    get inputDiv() {

        return this._inputDiv;

    }

    set inputDiv(value) {
        this._inputDiv = value;
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
        this._edited=false
        this._boilerPlateCodes = {};
        this._boilerPlateCodes["Java"] = "class Main {\n" +
            "    public static void main(String[] args) {\n" +
            "        System.out.println(\"Hello, World!\"); \n" +
            "    }\n" +
            "}"
        this._boilerPlateCodes["C"] = "#include <stdio.h>\n" +
            "int main()\n" +
            "{\n" +
            "   // printf() displays the string inside quotation\n" +
            "   printf(\"Hello, World!\");\n" +
            "   return 0;\n" +
            "}"
        this._boilerPlateCodes["Python"] = "print(\"Hello, World\")"
    }

    setInputTextArea(string) {
        this._inputsTextArea.value = string;
    }

    setEditorBoilerPlateCode(string) {
        this._editor.getDoc().setValue(string);

    }

    dropDownSelectAction() {
        if (this._edited==false || this._editor.getValue().length==0){
            this.setEditorBoilerPlateCode(
                this._boilerPlateCodes[this._dropDown.options[this._dropDown.selectedIndex].value]);
            this._edited=false
        }
    }


    checkboxAction() {
        if (this._checkbox.checked) {
            this._inputDiv.style.display = "block";
             this._runButton.disabled = true;
            this._submitButton.disabled = true;
        }
        else {
            this._inputDiv.style.display = "none";
            if (this._editor.getValue().length > 0) {
                this._runButton.disabled = false;
                this._submitButton.disabled = false;
            }




        }


    }

    inputsChanged() {
        if (this._inputsTextArea.value == NaN || this._inputsTextArea.value.length == 0) {
            this._runButton.disabled = true;
            this._submitButton.disabled = true;
        }
        else {
            this._runButton.disabled = false;
            this._submitButton.disabled = false;
        }
    }


    editorKeyUp(cm, event) {
        this._edited=true;
        if (!cm.state.completionActive && /*Enables keyboard navigation in autocomplete list*/
            event.keyCode != 13 && event.code != "Backspace") {
            /*Enter - do not open autocomplete list just after item has been selected in it*/
            CodeMirror.commands.autocomplete(cm, null, {completeSingle: false});

        }

        if (this._inputDiv.style.display == "None") {
            if (this._editor.getValue().length > 0) {
                this._runButton.disabled = false;
                this._submitButton.disabled = false;
            }
            else {
                this._runButton.disabled = true;
                this._submitButton.disabled = true;
            }

        }
        else if (this._editor.getValue().length > 0 &&
            this._inputsTextArea.value != NaN || this._inputsTextArea.value.length != 0) {
            this._runButton.disabled = false;
            this._submitButton.disabled = false;
        }
        else {

            this._runButton.disabled = true;
            this._submitButton.disabled = true;

        }
    }

    newThemeSelected(){
        this._editor.setOption("theme",this._themeSelect.options[this._themeSelect.selectedIndex].value);
        document.cookie="theme="+this._themeSelect.options[this._themeSelect.selectedIndex].value;
    }

    init(data,theme) {
        if(data.length==0) {
            this.setEditorBoilerPlateCode(this._boilerPlateCodes["Python"]);
        }
        else {
            this._editor.getDoc().setValue(data);
        }
        this.checkboxAction();
        this._edited=false;
        this._themeSelect.value=theme;

    }

}