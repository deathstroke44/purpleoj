class AddThemeSelect{
     constructor(mediator, id) {
        this.mediator = mediator;
        this.select = document.getElementById(id);
        this.mediator._themeSelect = this.select;
        this.select.addEventListener('change',function () {
            mediator.newThemeSelected();
        },false);
    }
}