/** @odoo-module */
import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";



publicWidget.registry.leaveCreationDetails = publicWidget.Widget.extend({
    selector: '.for_js_selector',
    events: {
        'change #leave_half_day': '_onChange_leave_half_day',
        'change #leave_start_date': 'calculate_total_days',
        'change #leave_end_date': 'calculate_total_days',
        'click #leave_creation_submit_btn': 'click_submit_button',
        'change #many2one_student': '_onChange_student',
    },

    _onChange_leave_half_day: function(){
        if ($('#leave_half_day').is(":checked")) {
            $('#leave_an_or_fn_label').show()
            $('#leave_an_or_fn').show()
            $('#leave_total_days').val(0.5)
            $("#leave_end_date").hide()
            $('#leave_end_date_label').hide()
        }
        else {
            $('#leave_an_or_fn_label').hide()
            $('#leave_an_or_fn').hide()
            $("#leave_end_date").show()
            $('#leave_end_date_label').show()
               this.calculate_total_days()
        }
    },



    calculate_total_days: function(){
        var start_date = new Date($('#leave_start_date').val())
        var end_date = new Date($('#leave_end_date').val())
        var start_date_milli = start_date.getTime()
        var end_date_milli = end_date.getTime()
        var total_days = (((end_date_milli - start_date_milli)/86400000)+1)
        if (total_days < 1){
            $('#leave_total_days').val(0);
            $('#leave_date_validation').text('Start date is greater than end date...!');
        }
        else{
            $('#leave_total_days').val(total_days)
            $('#leave_date_validation').text('')
        }
    },

    click_submit_button: function(e){
        var total_days = $('#leave_total_days').val()
        if (total_days == 0){
            e.preventDefault()
        }
    },

    _onChange_student: function(){
        var student_id = $('#many2one_student').val()
        if (student_id){
            jsonrpc('/leave/class', {
            'id':student_id,
            }).then(function(data){
            $('#many2one_class').val(data)
            })
        }
        else{
            $('#many2one_class').val('')
        }
    },

});


publicWidget.registry.leaveDetailsTable = publicWidget.Widget.extend({
    selector: '.for_row_selector',
    events: {
        'click .leave_details_table_row': '_onClick_leave_details_table_row',
    },

    _onClick_leave_details_table_row: function(e){
        var selected_row_id = e.currentTarget.children[0].childNodes[1].innerText
        window.location = `/leave/${selected_row_id}`;
    },
});









