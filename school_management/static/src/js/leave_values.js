/** @odoo-module */
import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";


//to get class corresponding to student
$('#many2one_student').change(function(){
    var student_id = $(this).val()
    jsonrpc('/leave/class', {
    'id':student_id,
    }).then(function(data){
    $('#many2one_class').val(data)
    })
})

//open leave details page when clicking on row
$('.leave_details_table_row').click(function(){
    var leave_id = $(this).children().children().html()
    window.location = `/leave/${leave_id}`;
})

//to calculate total days
function calculate_total_days(){
    var start_date = new Date($('#leave_start_date').val())
    var end_date = new Date($('#leave_end_date').val())
    var start_date_milli = start_date.getTime()
    var end_date_milli = end_date.getTime()
    var total_days = (((end_date_milli - start_date_milli)/86400000)+1)
    if (total_days < 1){
    $('#leave_total_days').val(0)
    $('#leave_date_validation').text('Start date is greater than end date...!')
    }
    else{
    $('#leave_total_days').val(total_days)
    $('#leave_date_validation').text('')
    }
}

//half day check box
$("#leave_half_day").change(function() {
        if ($(this).is(":checked")) {
            $('#leave_an_or_fn_label').show()
            $('#leave_an_or_fn').show()
            $('#leave_total_days').val(0.5)
            $("#leave_end_date").hide()
            $('#leave_end_date_label').hide()
        } else {
            $('#leave_an_or_fn_label').hide()
            $('#leave_an_or_fn').hide()
            $("#leave_end_date").show()
            $('#leave_end_date_label').show()
               calculate_total_days()
        }
    });


$('#leave_start_date').change(function(){
   calculate_total_days()
})
$('#leave_end_date').change(function(){
   calculate_total_days()
})









