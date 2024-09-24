/** @odoo-module */

//for adding rating fields to props
import { patch } from "@web/core/utils/patch";
import { Orderline } from "@point_of_sale/app/store/models";
patch(Orderline.prototype, {
   getDisplayData() {
       return {
           ...super.getDisplayData(...arguments),
            rating: this.product.product_rating,
       };
   },
});