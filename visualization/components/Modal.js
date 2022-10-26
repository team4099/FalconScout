class Modal {
    constructor (mainId, openId, closeId, formId){
        this.mainId = mainId
        this.openId = openId
        this.closeId = closeId
        this.formId = formId
        this.callBackOpen = function () {}
        this.callBackClose = function () {}
        this.formHTML = ""

    }

    setCallBackOpen(method){
        document.getElementById(this.openId).removeEventListener("click", this.callBackOpen)
        this.callBackOpen = method
        document.getElementById(this.openId).addEventListener("click", this.callBackOpen)
    }

    setCallBackClose(method){
        document.getElementById(this.closeId).removeEventListener("click", this.callBackClose)
        this.callBackClose = method
        document.getElementById(this.closeId).addEventListener("click", this.callBackClose)
        console.log("set")
    }

    set formHTML(HTML){
        document.getElementById(this.formId).innerHTML = HTML
    }
}

export { Modal }