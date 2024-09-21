/** @odoo-module */


import { patch } from "@web/core/utils/patch";
import { Order } from "@point_of_sale/app/store/models";
import { useService } from "@web/core/utils/hooks";

//console.log('++++',useService('orm'))
patch(Order.prototype, {
    setup(){
        super.setup(...arguments)
        console.log(this)
//        this.orm = useService("orm");
    },
//   async pay() {
////   total_discount += this.get_total_discount()
////   console.log(this.pos_session_id)
////        var total_discount_amount = await this.orm.call('pos.order', 'send_total_discount_pos',[])
//
//       return {
//           ...super.pay(...arguments)
//       };
//   },
});
