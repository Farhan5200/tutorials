/** @odoo-module */

import publicWidget from "@web/legacy/js/public/public_widget";
import wSaleUtils from "@website_sale/js/website_sale_utils";
import { jsonrpc } from "@web/core/network/rpc_service";

publicWidget.registry.websiteShopCart = publicWidget.Widget.extend({
    selector:'.website_shop_cart',
    events: {
        'click .qty_add': '_onClickQtyAdd',
        'click .qty_sub': '_onClickQtySub',
        'click .shop_cart': '_onClickShopCart',
    },

//    increases quantity
    _onClickQtyAdd: function(e){
        e.preventDefault()
        var shop_qty = Number($(e.currentTarget).prev().val())
        shop_qty += 1
        $(e.currentTarget).prev().val(shop_qty)
    },

//    decreases quantity
    _onClickQtySub: function(e){
        e.preventDefault()
        var shop_qty = Number($(e.currentTarget).next().val())
        if (shop_qty == 1){
            $(e.currentTarget).next().val(1)
        }
        else{
            shop_qty -= 1
            $(e.currentTarget).next().val(shop_qty)
        }
    },

//    adds the product to the cart
    async _onClickShopCart(e){
        var product_id = Number($(e.currentTarget).prev().html())
        var product_qty = Number($(e.currentTarget).parent().prev().find('.shop_qty').val())
        const callService = this.call.bind(this)
        console.log(callService)
        jsonrpc('/shop/cart/update_json', {
            product_id: product_id,
            add_qty: product_qty,
        }).then(function (data) {
            wSaleUtils.updateCartNavBar(data);
            wSaleUtils.showCartNotification(callService, data.notification_info);
        });
    },
});