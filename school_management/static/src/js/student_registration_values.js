/** @odoo-module */
import publicWidget from "@web/legacy/js/public/public_widget";


//event page
$(document).ready(function(){
    $('#permanent_address_same_as_above').click(function(){
        console.log($('#permanent_address_same_as_above').val())
        $('#test').toggle()
        })
})