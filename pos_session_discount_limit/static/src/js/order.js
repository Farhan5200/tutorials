/** @odoo-module */


import { patch } from "@web/core/utils/patch";
import { Order } from "@point_of_sale/app/store/models";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";


//checks the total discount given in a session if it is greater than limit given in settings shows warning and stops the flow
patch(Order.prototype, {
   async pay() {
   if (this.pos.config.set_session_wise_limit && this.get_total_discount()){
    var result = await this.env.services.orm.call('pos.order','send_total_discount_pos',[this.pos_session_id])
    var setting_limit = this.pos.config.session_wise_discount_limit
    var current_order_total_disc = this.get_total_discount()
    console.log(result)
    if (current_order_total_disc > setting_limit){
        this.env.services.popup.add(ErrorPopup, {
            title:"Error",
            body:"ttnoooo",
        });
    }
    else if((result+current_order_total_disc) > setting_limit){
         this.env.services.popup.add(ErrorPopup, {
            title:"Error",
            body:"greater",
        });
    }
    else{
        return {
           ...super.pay(...arguments)
       };
    }
    }
    else {
       return {
           ...super.pay(...arguments)
       };
       }
   },
});
