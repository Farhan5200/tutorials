/** @odoo-module */
import publicWidget from "@web/legacy/js/public/public_widget";

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
