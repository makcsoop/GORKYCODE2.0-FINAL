$(function () {
    // разрешаю
    $('#technicalSupportInputDeal').change(function () {
        if ($(this).prop('checked') === true) {
            $('#technicalSupportFormBtnSubmit').prop('disabled', false);
        }
        else {
            $('#technicalSupportFormBtnSubmit').prop('disabled', true);
        }
    });


    $('#technicalSupportForm').validate({
        // добавляем класс к обертке у элементов формы при валидации
        highlight: function (element, errorClass, validClass) {
            $(element).closest(".form-group")
                .removeClass(validClass)
                .addClass(errorClass);
        },
        unhighlight: function (element, errorClass, validClass) {
            $(element).closest(".form-group")
                .removeClass(errorClass)
                .addClass(validClass);
        },
        // выводим сообщение в шапку формы о наличии ошибок
        invalidHandler: function (event, validator) {
            // 'this' refers to the form
            var errors = validator.numberOfInvalids();
            if (errors) {
                var message = 'Проверьте, пожалуйста, правильность заполнения формы.';
                $(this).find("div.error-message").html(message);
                $(this).find("div.error-message").show();
            } else {
                $(this).find("div.error-message").hide();
            }
        },
        rules: {
            "TechnicalSupport[name]": {
                required: true
            },
            "TechnicalSupport[email]": {
                required: true,
                email: true
            },
            "TechnicalSupport[comment]": {
                required: true
            }
        },
        submitHandler: function (form, e) {
            e.preventDefault();
            $.ajax({
                url: $(form).attr('action'),
                type: 'POST',
                //dataType: 'json',
                data: $(form).serialize(),
                success: function (data) {
                    if (data.success) {
                        $(form).find('.error-message').hide();
                        $(form).find('.error-summary').remove();
                        $('.modal').modal('hide');
                        $(form).get(0).reset();
                        $('#modalOk').modal();
                    } else if (data.errors) {
                        var summary = '';
                        for (var i in data.errors) {
                            if (data.errors.hasOwnProperty(i)) {
                                if (i === 'verifyCode') {
                                    $(form).find('.captcha-image').trigger('click');
                                }
                                summary += '<span class="error">' + data.errors[i].join('<br>') + '</span><br>';
                            }
                        }
                        $(form).find('.error-message').text('Проверьте, пожалуйста, правильность заполнения формы.').show().after(
                            '<div class="error-summary">' + summary + '</div>'
                        );
                    }
                }
            });
        }
    });

});
