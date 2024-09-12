/** @odoo-module */
import publicWidget from "@web/legacy/js/public/public_widget";


publicWidget.registry.studentCreationDetails = publicWidget.Widget.extend({
    selector: '.student_creation_selector',
    events: {
        'click #permanent_address_same_as_above': '_onClick_permanent_address_same_as_above',
        'keyup #communication_street': '_onKeyup_communication_street',
        'keyup #permanent_street': '_onKeyup_permanent_street',
        'keyup #communication_city': '_onKeyup_communication_city',
        'keyup #permanent_city': '_onKeyup_permanent_city',
        'change #communication_country': '_onChange_communication_country',
        'change #permanent_country': '_onChange_permanent_country',
        'change #date_of_birth': '_onChange_date_of_birth',
    },

    _onClick_permanent_address_same_as_above: function(){
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
    },

    _onKeyup_communication_street: function(){
        if ($('#permanent_address_same_as_above').is(":checked")){
        $('#permanent_street').val($('#communication_street').val())
        }
        else{
            $('#permanent_street').val('')
        }
    },

    _onKeyup_permanent_street: function(){
        if ($('#permanent_address_same_as_above').is(":checked")){
            $('#communication_street').val($('#permanent_street').val())
        }
    },

    _onKeyup_communication_city: function(){
        if ($('#permanent_address_same_as_above').is(":checked")){
            $('#permanent_city').val($('#communication_city').val())
        }
        else{
            $('#permanent_city').val('')
        }
    },

    _onKeyup_permanent_city: function(){
        if ($('#permanent_address_same_as_above').is(":checked")){
            $('#communication_city').val($('#permanent_city').val())
        }
    },

    _onChange_communication_country: function(){
        if ($('#permanent_address_same_as_above').is(":checked")){
            $('#permanent_country').val($('#communication_country').val())
        }
        else{
            $('#permanent_country').val('dummy')
        }
    },

    _onChange_permanent_country: function(){
        if ($('#permanent_address_same_as_above').is(":checked")){
            $('#communication_country').val($('#permanent_country').val())
        }
    },

    //to calculate age
    _onChange_date_of_birth: function(){
        $('#age').val('')
        var dob_year = new Date($('#date_of_birth').val()).getFullYear()
        var current_year = new Date().getFullYear()
        var age = current_year - dob_year
        if (age < 4){
            alert('Age should be greater than 4')
        }
        else{
            $('#age').val(age)
        }

    },
});

publicWidget.registry.studentMainMenuTableRow = publicWidget.Widget.extend({
    selector: '.student_table_row',
    events: {
        'click .student_table_row': '_onClick_student_table_row',
    },

    //open student details while clicking on table row
    _onClick_student_table_row: function(e){
        var selected_student_id = $(e.currentTarget).children().children().html()
        window.location = `/student/${selected_student_id}`
    },
});
