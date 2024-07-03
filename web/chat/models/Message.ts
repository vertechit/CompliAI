import {v4} from 'uuid'
export interface IMessage {
    id:string
    userId:number
    message:string
    date:string
    type: 'request' | 'response' | 'user'
    markdown: object
}
export default class Messages {

    listMensage:IMessage[] = []
    constructor(){}

    addMessage(message:IMessage){
        this.listMensage.push({
            ...message,
            id:v4(),
            date:new Date().toLocaleDateString(`pt-br`,{month:'long',day:'2-digit', year:'numeric'}),
        })
    }
    addDotsLoading(){
        this.listMensage.push({
            id:v4(),
            type:'request',
            date:new Date().toLocaleDateString(`pt-br`,{month:'long',day:'2-digit', year:'numeric'}),
            message:'',
            userId:0,
            markdown: {}
        })
    }
    async removeDotLoading(){
        this.listMensage.pop()
    }
}