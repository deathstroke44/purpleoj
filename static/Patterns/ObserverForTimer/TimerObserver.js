class TimerObserver extends Observer{
    constructor(endTime,redirectUrl,timerField){
        super(endTime);
        this._redirectUrl=redirectUrl;
        this._timerField=document.getElementById(timerField);
    }
    update(time){

            var distance=this._endTime-time;
            var days = Math.floor(distance / (1000 * 60 * 60 * 24));
            var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((distance % (1000 * 60)) / 1000);

            if(minutes<10){
                minutes = "0" + minutes;
            }
            if(seconds<10){
                seconds = "0" + seconds;
            }

            if(days>0){
                this._timerField.innerHTML = days + " Day " + hours + ":" + minutes + ":" + seconds;
            }
            else if(days==0){
                this._timerField.innerHTML = hours + ":" + minutes + ":" + seconds;
            }
            else if (distance < 0) {
                clearInterval(x);
                this._timerField.innerHTML = "CONTEST STARTED";
                window.location = this._redirectUrl;
            }
        }




}