/** @odoo-module */


import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { patch } from "@web/core/utils/patch";

// to add new function to remove selected order lines
patch(Orderline.prototype, {
    removeLine() {
         //to get current order
        const order = this.env.services.pos.get_order();

        // Find the orderline to remove based on the full product name
        for (var i=0;i<order.orderlines.length;i++){
            if (order.orderlines[i].full_product_name == this.props.line.productName){
                order.removeOrderline(order.orderlines[i])
            }
        }
    }
});
