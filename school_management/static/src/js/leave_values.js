/** @odoo-module */
import publicWidget from "@web/legacy/js/public/public_widget";

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
//    sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
    if (total_days < 1){
    $('#leave_total_days').val(0)
//    $('#leave_date_validation').
    }
    else{
    $('#leave_total_days').val(total_days)
    }
}


$('#leave_half_day').click(function(){
        console.log($('#leave_half_day').val())
        $('#leave_an_or_fn_label').toggle()
        $('#leave_an_or_fn').toggle()
})

$('#leave_start_date').change(function(){
   calculate_total_days()
})
$('#leave_end_date').change(function(){
   calculate_total_days()
})



