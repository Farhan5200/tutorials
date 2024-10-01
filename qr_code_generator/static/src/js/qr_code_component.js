/** @odoo-module */
import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

class QRCode extends Component {
    suuuuuur(){
        console.log('kikijijijijk')
    }

}
QRCode.template = "qr_code_generator.qr_generator_modal"

registry.category("actions").add("qr_generator_modal",QRCode)
