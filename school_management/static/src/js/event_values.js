/** @odoo-module */
import publicWidget from "@web/legacy/js/public/public_widget";
console.log(publicWidget,"publicWidget")
var CustomForm = publicWidget.Widget.extend({
    selector: '.new-get_data',
    start: function () {
    $('.js-example-basic-multiple').select2();
    }
    });
publicWidget.registry.Many2many_tag = CustomForm;
return CustomForm;