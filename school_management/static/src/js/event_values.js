/** @odoo-module */
import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";


//when clicking edit button
$('#event_creation_update_btn').click(function(){
$('.event_show_page').prop("readonly", false);
$('#event_creation_save_btn').show()
$('#event_show_club').prop("disabled", false)
$(this).hide()
})


//when clicking save button
$('#event_creation_save_btn').click(function(e){
    var club_ids = $("#event_show_club").val()
    if (club_ids.length < 1){
        alert('Select at least one club');
        e.preventDefault();
        return false;
    }
    $('#event_show_club_id_storing').val(club_ids)
    $(this).hide()
    $('#event_creation_update_btn').show()
    $('.event_show_page').prop("readonly", true);

})

//delete button in row
$('.event_creation_row_delete_btn').click(function(){
    var selected_event_id = $(this).prev().html()
    jsonrpc('/event/delete', {
        'id': selected_event_id,
        })
})


//to delete selected event
$('#event_creation_delete_btn').click(function(){
    var selected_event_id = $('#selected_event_id_del').val()
    console.log(selected_event_id)
    jsonrpc('/event/delete', {
    'id': selected_event_id,
    })
    window.location = "/events"
})


//takes clicked event id and creates a redirect link
$('.events_table_row').click(function(){
    var event_id = $(this).parent().children().children().html()
    window.location = `/event/${event_id}`;
    })


//add values of many to many field to another field
$('#event_creation_submit_btn').click(function(){
    var club_ids = $("#many2many_club").val()
    console.log(club_ids)
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
console.log(CustomForm)
return CustomForm





