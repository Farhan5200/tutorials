/** @odoo-module */
import publicWidget from "@web/legacy/js/public/public_widget";


//address
$('#permanent_address_same_as_above').click(function(){
    if ($('#permanent_address_same_as_above').is(":checked")){
        $('#permanent_street').val($('#communication_street').val())
        $('#permanent_city').val($('#communication_city').val())
        $('#permanent_country').val($('#communication_country').val())
    }
    else{
        $('#permanent_street').val('')
        $('#permanent_city').val('')
        $('#permanent_country').val('dummy')
    }
    })
$('#communication_street').keyup(function(){
    if ($('#permanent_address_same_as_above').is(":checked")){
        $('#permanent_street').val($(this).val())
    }
    else{
        $('#permanent_street').val('')
    }
})
$('#permanent_street').keyup(function(){
    if ($('#permanent_address_same_as_above').is(":checked")){
        $('#communication_street').val($(this).val())
    }
})
$('#communication_city').keyup(function(){
    if ($('#permanent_address_same_as_above').is(":checked")){
        $('#permanent_city').val($(this).val())
    }
    else{
        $('#permanent_city').val('')
    }
})
$('#permanent_city').keyup(function(){
    if ($('#permanent_address_same_as_above').is(":checked")){
        $('#communication_city').val($(this).val())
    }
})
$('#communication_country').change(function(){
    if ($('#permanent_address_same_as_above').is(":checked")){
        $('#permanent_country').val($(this).val())
    }
    else{
        $('#permanent_country').val('dummy')
    }
})
$('#permanent_country').change(function(){
    if ($('#permanent_address_same_as_above').is(":checked")){
        $('#communication_country').val($(this).val())
    }
})


//age computation
$('#date_of_birth').change(function(){
    $('#age').val('')
    var dob_year = new Date($(this).val()).getFullYear()
    var current_year = new Date().getFullYear()
    var age = current_year - dob_year
    if (age < 4){
        alert('Age should be greater than 4')
    }
    else{
        $('#age').val(age)
    }

})

//open student details while clicking on table row
$('.student_table_row').click(function(){
    var selected_student_id = $(this).children().children().html()
    window.location = `/student/${selected_student_id}`
})