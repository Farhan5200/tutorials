/** @odoo-module */


import { patch } from "@web/core/utils/patch";
import { Order } from "@point_of_sale/app/store/models";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";


//checks the total discount given in a session if it is greater than limit given in settings shows warning and stops the flow
patch(Order.prototype, {
    async pay() {
        if (this.pos.config.set_session_wise_limit){
            //if set session wise limit is enabled in setting this if condition will work
            var current_order_total_disc=0
            var orderline_length = this.orderlines.length
            for (var i=0; i < orderline_length;i++){
                if (this.orderlines[i].price < 0 ){
                    //this adds the global discount value to the calculation
                    var tax_amount = await this.env.services.orm.call('pos.order','send_product_tax',[this.orderlines[i].product.id])
                    var global_discount = ((this.orderlines[i].price) * ((tax_amount+100)/100))
                    current_order_total_disc -= global_discount
                }
            };
            var result = await this.env.services.orm.call('pos.order','send_total_discount_pos',[this.pos_session_id]) // gets the current session total discount
            var setting_limit = this.pos.config.session_wise_discount_limit //gets the discount limit given in settings
            current_order_total_disc += this.get_total_discount() //gets the total discount of th current order
            if ((current_order_total_disc > setting_limit) || ((result+current_order_total_disc) > setting_limit)){
                this.env.services.popup.add(ErrorPopup, {
                    title:"Service Denied",
                    body:"Session total discount exceeded the limit...",
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
