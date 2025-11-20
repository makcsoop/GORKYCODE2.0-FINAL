$(function () {
    var currentUrl = window.location;
    var formModal = $('#spelling-modal');
    var selectedTextInput = $('#spelling-selectedtext');
    var selectedTextP = $('#spelling-selected-text');
    var spellingForm = $('#spelling-form');
    var submitButton = $('#spelling-submit-button');
    var commentBlock = $('#spelling-comment')
    var messageBlock = $('#spelling-message');
    var requestUrl = spellingForm.attr('action');
    var popupParams = {
        closeBtn: true,
        autoSize: false,
        fitToView: false,
        margin: 0,
        padding: 0,
        width: 'auto',
        height: "inherit",
        autoHeight: true,
    };

    $('#spelling-url').val(currentUrl);

    $(document).keydown(function (e) {
        var selectionText = getSelectionText();
        if (e.ctrlKey && 13 == e.which && selectionText) {
            if (selectionText.length > 500) {
                alert('Выделен слишком длинный текст. Пожалуйста, выделите менее 500 символов.');
            } else {
                normalizeForm();
                selectedTextInput.val(selectionText);
                selectedTextP.text(selectionText);
                //$.fancybox($(formModal), popupParams);
                $(formModal).modal('show');
            }
        }
    });


    spellingForm.validate({
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
            "Spelling[url]": {
                required: true,
                is_url: true
            },
            "Spelling[selectedText]": {
                required: true
            },
            "Spelling[comment]": {
                required: true
            }
        },
        submitHandler: function (form, e) {
            e.preventDefault();
            $.ajax({
                url: $(form).attr('action'),
                type: 'POST',
                data: $(form).serialize(),
                //dataType: 'JSON',
                beforeSend: function () {
                    submitButton.prop('disabled', true);
                },
                success: function (data) {
                    console.log(data);
                    if (data.success) {
                        $(form).find('.error-message').hide();
                        $(form).find('.error-summary').remove();
                        $(formModal).modal('hide')
                        $('#modalOk').modal();
                    } else if (data.errors) {

                        var summary = '';
                        for (var i in data.errors) {
                            if (data.errors.hasOwnProperty(i)) {
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

    function getSelectionText() {
        var txt = '';
        if (typeof window.getSelection !== 'undefined') {// Не IE, используем метод getSelection
            txt = window.getSelection().toString();
        } else if (typeof document.selection !== 'undefined') { // IE, используем объект selection
            txt = document.selection.createRange().text;
        }
        return txt;
    }

    function normalizeForm() {
        messageBlock.addClass('hidden').removeClass('alert-danger', 'alert-success').text('');
        selectedTextInput.val('');
        selectedTextInput.val('');
        commentBlock.val('');
        submitButton.prop('disabled', false);
    }
});
