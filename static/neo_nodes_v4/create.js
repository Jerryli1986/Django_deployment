
$(document).ready(function(){
    var prefix=String('form');
    $('.add-form-row').click(function(e){
        e.preventDefault();
        var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
        if (formCount>0) {
            var row = $(".item:last").clone(false).get(0);
            $(row).insertAfter(".item:last").slideDown(300);

            $(row).find('.formset-field').each(function () {
                // remove value cloned from last one
                $(this).val('');
                //	change id name
                updateElement(this, prefix, formCount);

            });
            $(row).find('.remove-form-row').each(function () {
                updateElement(this, prefix, formCount);

            });
        }
        else {
            var newIn = '<tr class="item">'+
              '<td>'             +
              '<input name="form-0-attr_name" class="formset-field" id="id_form-0-attr_name" type="text" maxlength="100">'+
              '</td>' +
              '<td>' +
               '<input name="form-0-attr_value" class="formset-field" id="id_form-0-attr_value" type="text" maxlength="100">'+
              '</td>' +
              '<td>'  +
                '<button type="button" class="btn btn-danger btn-sm remove-form-row" id="form-0">-</button>' +
              '</td>' +
            '</tr >' ;
           var newInput = $(newIn);
            (newInput).insertAfter($('#t1'))
        }
     var forms = $('.item'); // Get all the forms
        // Update the total number of forms (1 less than before)
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);

    });


    $("body").on('click', '.remove-form-row',function () {
        // Delete the item/form
        $(this).parents('tr').remove();

        // update id and name
        var forms = $('.item'); // Get all the forms
        // Update the total number of forms (1 less than before)
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        var i = 0;
        // Go through the forms and set their indices, names and IDs
        for (formCount = forms.length; i < formCount; i++) {
            $(forms.get(i)).find('.formset-field').each(function () {
                updateElement(this, prefix, i);

            });
            $(forms.get(i)).find('.remove-form-row').each(function () {
                updateElement(this, prefix, i);

            });
        }
    });
    function updateElement(el, prefix, ndx) {
        var id_regex = new RegExp(prefix + '-\\d+');
        var replacement = prefix + '-' + ndx;
        if (el.id)
            el.id = el.id.replace(id_regex, replacement);
        if (el.name)
            el.name = el.name.replace(id_regex, replacement);
    }
});