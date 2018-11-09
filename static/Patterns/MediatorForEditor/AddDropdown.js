class AddDropdown {
     constructor(mediator, id) {
        this.mediator = mediator;
        this.select = document.getElementById(id);
        this.mediator._dropDown = this.select;
        this.select.addEventListener('change',function () {
            mediator.dropDownSelectAction();
        },false);
         if (this.getCookie("language") != "") {
             this.select.value = this.getCookie("language")
         }

    }

    getCookie(cname) {

        var name = cname + "=";
        var decodedCookie = decodeURIComponent(document.cookie);
        var ca = decodedCookie.split(';');
        for (var i = 0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) == ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
    }

}