/** @odoo-module */
import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";
//var TestController = PublicWidget.Widget.extend({
//   willStart: async function () {
//           const data = await jsonrpc('/event/delete', {})
//       },
//});

//var ajax = require('web.ajax');

$('#event_creation_test_btn').click(function(){
    jsonrpc('/event/delete', {
    'id':8
    }).then(function(data){
    console.log(data)
    })
})


//takes clicked event id and creates a redirect link
$('.events_table_row').click(function(){
    var event_id = $(this).children().children().html()
    window.location = `/event/${event_id}`;
    })

//add values of many to many field to another field
$('#event_creation_submit_btn').click(function(){
    var club_ids = $("#many2many_club").val()
    $('#club_id_storing').val(club_ids)
})

//attaches the many2many tag widget to many 2 many field
var CustomForm = publicWidget.Widget.extend({
    selector: '.new-get_data',
    start: function () {
    $('.js-example-basic-multiple').select2();
    }
    });
publicWidget.registry.Many2many_tag = CustomForm;



//publicWidget.registry.schoolEventDetails = publicWidget.Widget.extend({
//    selector: '.event_details_test',
//    events: {
//        'change select[name="country_id"]': '_onCountryChange',
//          'click #event_creation_submit_btn': '_clickSubmit',
//    },
//
//    })
