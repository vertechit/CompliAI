import {defineStore } from 'pinia'

export const defaultStore = defineStore('defaultStoreId',{
    state: ()=> ({
        loading:false
    }),
    getters:{
        getLoading:(state) => state.loading 
    },
    actions:{
        setLoading(payload:boolean) {
            this.loading = payload
        }
    }
})