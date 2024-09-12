/** @odoo-module */

import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";


publicWidget.registry.eventShowDetails = publicWidget.Widget.extend({
    selector: '.event_details_selector',
    events:{
        'click #event_creation_update_btn': '_onClick_event_creation_update_btn',
        'click #event_creation_save_btn': '_onClick_event_creation_save_btn',
        'click #event_creation_delete_btn': '_onClick_event_creation_delete_btn',

    },

    //for selecting multiple options in club selection field
    start: function () {
    $('.many2many_select').select2();
    },

    //when clicking edit button
    _onClick_event_creation_update_btn: function(){
        $('.event_show_page').prop("readonly", false);
        $('#event_creation_save_btn').show()
        $('#event_show_club').prop("disabled", false)
        $('#event_creation_update_btn').hide()
    },

    //when clicking save button
    _onClick_event_creation_save_btn: function(e){
        console.log('iiii')
        var club_ids = $("#event_show_club").val()
        if (club_ids.length < 1){
            alert('Select at least one club');
            e.preventDefault();
            return false;
        }
        $('#event_show_club_id_storing').val(club_ids)
        $('#event_creation_save_btn').hide()
        $('#event_creation_update_btn').show()
        $('.event_show_page').prop("readonly", true);
    },

    //to delete selected event
    _onClick_event_creation_delete_btn: function(){
        var selected_event_id = $('#selected_event_id_del').val()
        console.log(selected_event_id)
        jsonrpc('/event/delete', {
        'id': selected_event_id,
        }).then((result) => {
        window.location.reload()
        window.location = "/events"})
    }
});


publicWidget.registry.eventCreationDetails = publicWidget.Widget.extend({
    selector: '.event_creation_selector',
    events:{
        'click #event_creation_submit_btn': '_onClick_event_creation_submit_btn',
    },

    //attaches the many2many tag widget to many 2 many field
    start: function () {
        $('.js-example-basic-multiple').select2();
    },

    //add values of many to many field to another field
    _onClick_event_creation_submit_btn: function(){
        var club_ids = $("#many2many_club").val()
        console.log(club_ids)
        $('#club_id_storing').val(club_ids)
    },
});

publicWidget.registry.eventMainMenuTableRow = publicWidget.Widget.extend({
    selector: '.event_main_menu_row_selector',
    events: {
        'click .events_table_row': '_onClick_events_table_row',
        'click .event_creation_row_delete_btn': '_onClick_event_creation_row_delete_btn',
    },

    //takes clicked event id and creates a redirect link
    _onClick_events_table_row: function(e){
        var event_id = $(e.currentTarget).parent().children().children().html()
        window.location = `/event/${event_id}`;
    },

    //delete button in row
    _onClick_event_creation_row_delete_btn: function(e){
        var selected_event_id = $(e.currentTarget).prev().html()
        jsonrpc('/event/delete', {
            'id': selected_event_id,
            }).then((result) => {
                window.location.reload()})
    },
});
