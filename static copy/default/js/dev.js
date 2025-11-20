/**
 * Created by krok on 02.07.17.
 */

jQuery(function ($) {
    $('.mpz__scroll').each(function(){
        psPanel = new PerfectScrollbar(this); 
    })

    $('.custom-tab-item a').click(function(){
        setTimeout(function () {
            $('.mpz__scroll').each(function(){
                psPanel = new PerfectScrollbar(this); 
            })
        }, 2000);
        
    });
    

    $('.interval-calendar__input').datepicker({
        range: 'period', // режим - выбор периода
        numberOfMonths: 2,
        onSelect: function (dateText, inst, extensionRange) {
            $('.interval-calendar__input').val(extensionRange.startDateText + " - " + extensionRange.endDateText);
        }

    })
    $('body').on("click", ".ui-datepicker-reset", function () {
        $('.interval-calendar__input').val('');
        $.datepicker._hideDatepicker();
    });
    $('.interval-calendar__discharge').click(function () {
        $('.interval-calendar__input').val('');
    });

    var $body = $('body');

    $('[data-ajax]').on('click', function (e) {
        e.preventDefault();

        var $a = $(this);

        $.ajax({
            url: $a.attr('href'),
            method: 'GET',
            cache: false,
            beforeSend: function () {
                $a.trigger('ajax.beforeSend');
            },
            success: function (data) {
                $a.trigger('ajax.success', [data]);
            }
        });
    });

    $('[form-ajax]').on('submit', function (e) {
        e.preventDefault();

        var $form = $(this);

        $.ajax({
            url: $form.attr('action'),
            method: $form.attr('method'),
            data: $form.serialize(),
            cache: false,
            beforeSend: function () {
                $form.trigger('ajax.beforeSend');
            },
            success: function (data) {
                $form.trigger('ajax.success', [data]);
            }
        });
    });

    var $html = $('html');

    $html.on('blind.set.fontSize', function (e, fontSize) {
        $.cookie('blind-fontSize', fontSize, {expires: 30, path: '/'});
    });

    $html.on('blind.set.colorSchema', function (e, colorScheme) {
        $.cookie('blind-colorSchema', colorScheme, {expires: 30, path: '/'});
    });

    $html.on('blind.set.imgDisplay', function (e, colorScheme) {
        $.cookie('blind-imgDisplay', colorScheme, {expires: 30, path: '/'});
    });

    $html.on('blind.set.kerning', function (e, colorScheme) {
        $.cookie('blind-kerning', colorScheme, {expires: 30, path: '/'});
    });

    $html.on('blind.set.garniture', function (e, colorScheme) {
        $.cookie('blind-garniture', colorScheme, {expires: 30, path: '/'});
    });


    $html.on('blind.unset.fontSize', function (e, fontSize) {
        $.cookie('blind-fontSize', fontSize, {expires: 30, path: '/'});
    });

    $html.on('blind.unset.colorSchema', function (e, colorScheme) {
        $.cookie('blind-colorSchema', colorScheme, {expires: 30, path: '/'});
    });

    $html.on('blind.unset.imgDisplay', function (e, colorScheme) {
        $.cookie('blind-imgDisplay', colorScheme, {expires: 30, path: '/'});
    });

    $html.on('blind.unset.kerning', function (e, colorScheme) {
        $.cookie('blind-kerning', colorScheme, {expires: 30, path: '/'});
    });

    $html.on('blind.unset.garniture', function (e, colorScheme) {
        $.cookie('blind-garniture', colorScheme, {expires: 30, path: '/'});
    });


    $(document).ajaxSuccess(function (event, xhr, settings) {
        if (settings.url.indexOf("/cabinet/favorite/default/delete") == 0) {
            var $this = event.currentTarget.activeElement;
            $($this).closest('.post-list.post-list--with-delete').remove();
            if ($('.post-list--with-delete').length == 0) {
                $('.post-list--style-i').html('<p>Нет материалов, добавленных в "Избранное".</p>');
            }
        }
    });


    $.fancybox.defaults.i18n.ru = {
        CLOSE: 'Закрыть',
        NEXT: 'Вперед',
        PREV: 'Назад',
        ERROR: "Ошибка загрузки контента. <br/> Попробуйте повторить позже.",
        PLAY_START: "Начать слайдшоу",
        PLAY_STOP: "Остановить слайдшоу",
        FULL_SCREEN: "Полный экран",
        THUMBS: "Эскизы",
        DOWNLOAD: "Скачть",
        SHARE: "Поделиться",
        ZOOM: "Увеличить"
    };

    $.fancybox.defaults.lang = 'ru';

    $.fancybox.defaults.share = {
        tpl:
        '<div class="ya-share2 ya-share2_inited" data-services="vkontakte,facebook,odnoklassniki,twitter">' +
        '<div class="ya-share2__container ya-share2__container_size_m">' +
        '<h3 style="margin-bottom: 5px;">{{SHARE}}</h3>' +
        '<ul class="ya-share2__list ya-share2__list_direction_horizontal">' +
        '<li class="ya-share2__item ya-share2__item_service_vkontakte">' +
        '<a class="ya-share2__link" href="https://vk.com/share.php?url={{src}}&title={{descr}}" rel="nofollow noopener" target="_blank" title="ВКонтакте">' +
        '<span class="ya-share2__badge"><span class="ya-share2__icon"></span><span class="ya-share2__counter"></span></span><span class="ya-share2__title">ВКонтакте</span>' +
        '</a>' +
        '</li>' +
        '<li class="ya-share2__item ya-share2__item_service_facebook">' +
        '<a class="ya-share2__link" href="https://www.facebook.com/sharer.php?src=sp&u={{src}}&title={{descr}}&utm_source=share2" rel="nofollow noopener" target="_blank" title="Facebook">' +
        '<span class="ya-share2__badge"><span class="ya-share2__icon"></span><span class="ya-share2__counter"></span></span><span class="ya-share2__title">Facebook</span>' +
        '</a>' +
        '</li>' +
        '<li class="ya-share2__item ya-share2__item_service_odnoklassniki"><a class="ya-share2__link" href="https://connect.ok.ru/offer?url={{src}}&title={{descr}}&utm_source=share2" rel="nofollow noopener" target="_blank" title="Одноклассники">' +
        '<span class="ya-share2__badge"><span class="ya-share2__icon"></span><span class="ya-share2__counter"></span></span><span class="ya-share2__title">Одноклассники</span>' +
        '</a>' +
        '</li>' +
        '<li class="ya-share2__item ya-share2__item_service_twitter">' +
        '<a class="ya-share2__link" href="https://twitter.com/intent/tweet?text={{descr}}&url={{src}}&utm_source=share2" rel="nofollow noopener" target="_blank" title="Twitter">' +
        '<span class="ya-share2__badge"><span class="ya-share2__icon"></span></span><span class="ya-share2__title">Twitter</span>' +
        '</a>' +
        '</li>' +
        '</ul>' +
        '</div>' +
        '</div>'
    };
}(jQuery));
