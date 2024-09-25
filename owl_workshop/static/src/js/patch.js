/**@odoo-module*/
import { InputBox } from "./input_box"
import { patch } from "@web/core/utils/patch";
import { useState } from "@odoo/owl";
import { useEffect } from "@odoo/owl";
import { useRef } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";




patch(InputBox.prototype, {
    setup() {
        super.setup()
        this.state = useState({
            value: 0,
        })
        useEffect(
            () => {
                    this.demo()
            },
            () => [this.state.value]
        );
        this.action = useService("action");
        this.input_boxoo = useRef('input_box_text')
        this.orm = useService("orm");
        this.datass = this.fetch_data()
//        console.log(this.datass)

    },
    demofu(e){
        this.state.value += e
    },
    demo(){
        console.log('useeffect')
    },
//    action service
    async input_valoo(){
        this.input_boxoo.el.value='iii'
        await this.orm.call('payment.provider','demoooo',[18])
        this.action.doAction({
                type: 'ir.actions.act_window',
                res_model: 'sale.order',
                res_id: 41,
                views: [[false, "form"]],
                view_mode: "form",
                target: "new",
            });
    },
    async fetch_data(){
        var datasss = await this.orm.call('dem.dem', 'sales',[11])
//        var datasss = await  this.orm.search("sale.order", [], { limit: 10 })
//        var datasss = await  this.orm.searchRead("sale.order",[],[], { limit: 10 })
        console.log(datasss)
    },
});