$(document).ready(function() {
    
    // проверка почты
    $.validator.addMethod("is_email", (function(value, element, param) {
        var email;
        email = value.match(/^((([0-9A-Za-z]{1}[-0-9A-z\.]{1,}[0-9A-Za-z]{1})|([0-9А-Яа-я]{1}[-0-9А-я\.]{1,}[0-9А-Яа-я]{1}))@([-A-Za-z]{1,}\.){1,2}[-A-Za-z]{2,})$/u);
        return this.optional(element) || email;
    }), "Email введен некорректно");

    // проверка логина
    $.validator.addMethod("is_login", (function(value, element, param) {
        var login;
        login = value.match(/^[a-zA-Z0-9]+$/);
        return this.optional(element) || login;
    }), "Логин может содержать только латинские символы и цифры");

    // буквы
    $.validator.addMethod("is_letter", (function(value, element, param) {
        var letter;
        letter = value.match(/^[а-яёa-z ]+$/gi);
        return this.optional(element) || letter;
    }), "Это поле может содержать только буквы");

});
