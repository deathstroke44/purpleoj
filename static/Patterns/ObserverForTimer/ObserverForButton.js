class ObserverForButton extends  Observer{
    constructor(endTime,buttonID){
        super(endTime);
        this._button=document.getElementById(buttonID);
    }

    update(time){
        window.alert("updating");
        var distance = this._endTime - time;
        if(distance > 0){
            window.alert("submit available");
            this.button.style.display = 'block'
        }
        else {
            window.alert("submit NOT available");
            this._button.style.display = 'none'
        }
    }
}