class Observer {
    constructor(endTime) {
        if (new.target === Observer) {
            throw new TypeError("Cannot construct Abstract instances directly");
        }

        this._endTime = endTime

    }

    update(time) {

    }

}