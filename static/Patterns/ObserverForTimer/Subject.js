class Subject{

    constructor(){
        this._previosTime=new Date().getTime();
        this._array=[];
    }
    changeState(time){

            if(time-this._previosTime>=1000){

                for(var i=0;i<this._array.length;i++){
                    this._array[i].update(time);
                }
                this._previosTime=time;
            }
        }

    attach(observer){

        this._array.push(observer);

    }

}