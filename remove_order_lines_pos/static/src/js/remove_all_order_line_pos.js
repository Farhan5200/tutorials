/** @odoo-module */

import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { Component } from "@odoo/owl";

export class RemoveAllOrderLineButton extends Component {
    static template = "remove_order_lines_pos.RemoveAllOrderLineButton";
    //to clear complete orderline
    removeAllOrderLine() {
        const order = this.env.services.pos.get_order();
        while(order.orderlines.length > 0){
            for (var i=0;i<order.orderlines.length;i++){
                    order.removeOrderline(order.orderlines[i])
            }
        }
    }
};

ProductScreen.addControlButton({
component: RemoveAllOrderLineButton,
});
