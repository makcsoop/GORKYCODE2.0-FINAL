(function () {

    $('[data-toggle="tooltip"]').tooltip({
        delay: { show: 100, hide: 10 }
    });
    $('.tooltip-download').on('show.bs.tooltip', function () {
        if($(this).width() > $(this).find('.name').width()) {
            $(this).tooltip('destroy');
        } 
    });

    $(".modal-doc").fancybox({
        fitToView   : false,
        width       : '70%',
        height      : '70%',
        autoSize    : false,
        closeClick  : false,
        openEffect  : 'none',
        closeEffect : 'none',
        type: 'iframe',
    });

    $(".modal-text").fancybox({
        fitToView   : false,
        width       : '70%',
        height      : '70%',
        autoSize    : false,
        closeClick  : false,
        openEffect  : 'none',
        closeEffect : 'none',
    });

    if($('.widget-slider').length) {
        $('.widget-slider').slick({
            slidesToShow: 1,
            slidesToScroll: 1,
            dots: true,
            fade: true,
            arrows: false,
            infinite: true,
            autoplay: true,
            autoplaySpeed: 20000,
            pauseOnFocus: true,
            pauseOnHover: true,
            focusOnSelect: true,
            appendDots: '.widget-slider__nav',     
        })
    }

    if($('.slider-main').length) {
        var mainSliderIndicator = $('.slider-main-indicator'),
            mainSliderSpeed = 5000;
        $('.slider-main').slick({
            slidesToShow: 1,
            slidesToScroll: 1,
            fade: true,
            dots: true,
            arrows: false,
            infinite: true,
            autoplay: true,
            autoplaySpeed: mainSliderSpeed,
            appendDots: '.slider-main__nav',
            pauseOnFocus: false,
            pauseOnHover: false
        }).on('beforeChange init', function(event, slick, currentSlide, nextSlide){
            mainSliderIndicator.animate({width: '0'}, 10);
        }).on('afterChange', function(event, slick, currentSlide){
            mainSliderIndicator.animate({width: '100%'}, mainSliderSpeed);
        });
    }

    if($('.area-promo-slider').length) {
        $('.area-promo-slider').slick({
            slidesToShow: 1,
            slidesToScroll: 1,
            dots: false,
            arrows: true,
            infinite: true,
            autoplay: true,
            autoplaySpeed: 7000,
            pauseOnFocus: false,
            pauseOnHover: false,
            centerMode: true,
            focusOnSelect: true,
            variableWidth: true,      
            nextArrow: '.area-promo-slider__nav .next',
            prevArrow: '.area-promo-slider__nav .prev',
            responsive: [
            {
                breakpoint: 1370,
                settings: {
                    slidesToShow: 1,
                    fade: true,
                    centerMode: false,
                    variableWidth: false
                }
            }
        ]
        }).on('afterChange', function(event, slick, currentSlide){
            areaPromoTimer();
        });
        function areaPromoTimer(){
            $('#timer-prime').circleProgress({
                value: 1,
                thickness: 2,
                size: 60,
                fill: 'rgba(233,75,61,.8)',
                emptyFill: 'rgba(255,255,255,0)',
                animation: { duration: 7000, easing: "circleProgressEasing" }
            });
        }
        areaPromoTimer();
    }

    var winWidth = $(window).width();

    $(document).ready(function(){
        if($(window).width() <= 670) {
            $('.slide-mobile').slick({
                slidesToShow: 1,
                slidesToScroll: 1,
                fade: false,
                dots: true,
                arrows: false,
            });
        }
    });

    $(window).on('load resize orientationChange', function(event) {
        if ($(window).width() != winWidth) {
            winWidth = $(window).width();
            setTimeout(function(){
                if($(window).width() > 670) {
                    $('.slide-mobile').each(function(){
                        $(this).slick('unslick');
                    });
                }
                else {
                    $('.slide-mobile').each(function(){
                        $(this).slick({
                            slidesToShow: 1,
                            slidesToScroll: 1,
                            fade: false,
                            dots: true,
                            arrows: false,
                        });
                    });
                }
            }, 200);
        }
    });


    $('li.dropdown-hover').hover(function() {
        if(!$('#panelMap').hasClass('open') && $(this).find('.list-division li').length !== 0){
            $(this).find('.dropdown-hover-box').stop(true, true).delay(200).fadeIn(200).addClass('open');
        }
    }, function() {
        $(this).find('.dropdown-hover-box').stop(true, true).delay(200).fadeOut(200).removeClass('open');
    });

    $(function() {

        $('.droptarget').on("dragenter dragover", function() {
            $(this).addClass('drop');
        }).on("dragleave mouseleave", function() {
            $(this).removeClass('drop');
        });
    });


    /* tab more */

    // прячем элементы навигации при ресайзе
    function navComponent() {
        var _this = this;

        // задаем контейнеру объектов ширину
        this.setContainerWidth = function (container, containerParent, containerNeighbour, navElemString, navContainerString) {
            container.each(function () {
                var elem = this,
                    elemWidth;
                elemWidth =
                    containerParent.outerWidth() -
                    containerNeighbour.outerWidth() - 50;
                container.css({
                    'width': elemWidth + 40 + 'px',
                });
                //}
            });

            _this.adaptNav(container, navElemString, navContainerString);
        };


        // высчитываем общую ширину всех блоков внутри контейнера
        this.adaptNav = function (container, navElemString, navContainerString) {
            container.each(function () {
                var elem = $(this),
                    navElem = container.find(navElemString),
                    navContainer = container.find(navContainerString),
                    compareCounter = 1,
                    allNavElemWidth = 0;

                for (var i = 0; i < navElem.length; i++) {
                    allNavElemWidth += navElem.eq(i).outerWidth() +
                        parseInt(navElem.eq(i).css('margin-left')) +
                        parseInt(navElem.eq(i).css('margin-right'));

                    if (elem.outerWidth() < allNavElemWidth + 50) {
                        compareCounter++;
                    }


                }

                _this.compareContainerElemWidth(
                    container,
                    navElemString,
                    allNavElemWidth,
                    navContainer,
                    compareCounter);
            });
        };

        // прячем лишние блоки в несколько итераций.
        this.compareContainerElemWidth = function (container, navElemString, elemWidth, navContainer, counts) {
            navContainer.find('> ' + navElemString).insertBefore(navContainer.parent());

            for (var i = 1; i < counts; i++) {
                container.find('> ' + navElemString).eq(-1).prependTo(navContainer);
            }
        };

        // по клику на ссылку вытаскиваем её из родителя и закидываем после ссылки "все"
        this.showActiveElem = function (container, navElemString, elem) {
            var allElem = container.find(">" + navElemString).eq(0);

            elem.insertAfter(allElem);
        };

        // инициализируем все эти операции
        this.init = function (container, containerParent, containerNeighbour, navElemString, navContainerString) {
            _this.setContainerWidth(container, containerParent, containerNeighbour, navElemString, navContainerString);
        };
    }

    var navComponentVar = new navComponent();

    function checkTabsContainer() {
        $('.tabs-container').each(function () {
            var elem = $(this),
                containerElems = elem.find('.custom-tab-item');

            if (containerElems.length != 0) {
                elem.addClass('container-active');
            } else {
                elem.removeClass('container-active');
            }
        })
    }

    var navComponentTimeout;

    function initNavComponent() {
        clearTimeout(navComponentTimeout);
        navComponentTimeout = setTimeout(function () {
            $('.nav-tabs').each(function () {

                navComponentVar
                    .init(
                        $(this),
                        $(this).parents('.tabs-nav-wrap'),
                        $(this).parents('.tabs-nav-wrap').find('.section-head').eq(0),
                        '.custom-tab-item',
                        '.tabs-container__content');
            });
            checkTabsContainer();
        }, 10);
    }

    // навигация в шапке
    function initHeaderNav(){
        // прячем пункты в меню, если не умещаются в строку
        var headerNav = $('#headerNav'),
            maxWidth = headerNav.width(),
            widthLi = 0;
        // headerNav.css({'opacity': 0});
        $('#headerNav > li').each(function (i, el) {
            widthLi += $(this).outerWidth();
            if (widthLi <= maxWidth - 70) {
                $(this).show();
                $('.header-nav-more').removeClass('active');
            }
            else {
                $(this).hide();
                $('.header-nav-more').addClass('active');
            }
        });
        headerNav.css({'opacity': 1});
    }

    var windowWidth = $(window).width();
    $(window).on('load', function () {
        initNavComponent();
        initHeaderNav();
    });
    $(window).on('resize', function () {
        if ($(window).width() != windowWidth) {
            windowWidth = $(window).width();
            setTimeout(function () {
                initNavComponent();
                initHeaderNav();
            }, 100);
        }
    });

    // Функция для перекидывания активного таба после первого элемента навигации
    function showActiveElemEvnt(container, containerParent, containerNeighbour, navElemString, navContainerString, targetElem) {
        navComponentVar.showActiveElem(container, navElemString, targetElem);

        navComponentVar
            .setContainerWidth(container, containerParent, containerNeighbour, navElemString, navContainerString);

    }

    // обработчик события перекидывания активного таба после первого элемента навигац
    var shit = function () {
        $('.tabs-container .custom-tab-item').removeClass('active');
        var elem = $(this),
            elemParent = elem.parents('.nav-tabs').eq(0);
        
        showActiveElemEvnt(elemParent,
            elemParent.parents('.tabs-nav-wrap'),
            elemParent.parents('.tabs-nav-wrap').find('.section-head').eq(0),
            '.custom-tab-item',
            '.tabs-container__content', elem);

        // удаляем обработчик события, чтобы не было ненужных срабатываний на перемещенных блоках
        $('.custom-tab-item').unbind('click', shit);
    }


    // по клику на контейнер табов, накидываем события на все табы внутри этого контейнера
    $('.tabs-container__btn').click(function () {

        // кидаем обработчик событий
        $('.tabs-container .custom-tab-item').on('click', shit);
    });


    // text error on content page show modal
    function textError(selectedText) {

        // get page URL
        $('#textErrorPageUrlTag').text(window.location.href)
        $('#textErrorPageUrl').val(window.location.href);

        // get selected text
        $('#textErrorContentTextTag').text(selectedText);
        $('#textErrorContentText').val(selectedText);


        $('#textErrorModal').modal('show');
    }

    if ($('#textErrorModal').length != 0) {

        $(document).keydown(function (e) {
            if ((e.ctrlKey == true) && (e.keyCode == 13 || e.keyCode == 10)) {
                var selected_text = window.getSelection();
                if (selected_text != '') {
                    textError(selected_text);
                }
            }
        });
    }


    // в формах в списке с чекбоксами .all-check-parent
    // при выборе чекбокса .all-check с остальных снимаем чек
    $('.all-check').change(function () {
        var $this = $(this),
            parent = $this.closest('.all-check-parent'),
            check = $this.prop('checked');
        if (check === true) {
            parent.find(':checkbox').not($this).prop('checked', false).trigger('refresh');
        }
        else {
            return false;
        }
    });
    // если чекаем из списка чекбос не .all-check, снимаем чек с .all-check
    $('.all-check-parent :checkbox:not(.all-check)').change(function () {
        $(this).closest('.all-check-parent').find('.all-check').prop('checked', false).trigger('refresh');
    });


    // расчет макс высоты в блоках с доками
    $.fn.funcHeightMax = function (options) {
        this.each(function (options) {
            var obj = this;

            $(obj).on('load resize render', function () {
                var docsMinHeight = 0;
                var lengthDocs = $(obj).find('.docs-preview').length;
                setTimeout(function(){
                    $('.docs-preview', obj).each(function (i) {
                        var thisHeight = $(this).height();
                        if (docsMinHeight < thisHeight) {
                            docsMinHeight = thisHeight;
                        }
                        if (i === (lengthDocs - 1)) {
                            $('.docs-preview', obj).css({'min-height': docsMinHeight});
                            if (docsMinHeight < 240) {
                                $(obj).addClass('sm');
                            }
                            else {
                                $(obj).removeClass('sm');
                            }
                        }
                    });
                }, 50);
            });
            $(obj).trigger('load');
        });
    }

    if ($('.docs-preview-main').length > 0) {
        $('.docs-preview-main').funcHeightMax();
        $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
            $('.docs-preview-main').trigger('render');
        });
    }


    // filter
    var filterOpen = false,
        filter = $('#filter').length > 0 ? $('#filter') : false,
        filterBtn = $('#filterBtn');
        //btnBoxText = filterBtn.find('.filter-btn__text');

    function openFilter(){
        if(filterOpen){   
            filter.removeClass('open');
            filter.fadeOut(300);
            filterBtn.removeClass('active');
            //btnBoxText.html(filterBtn.data('open'));
            $('body').removeClass('filter-open');
            setTimeout(function(){
                $(window).scrollTop($('.main').offset().top + 50);    
            }, 300);
            filterOpen = false;
        } 
        else {
            filter.addClass('open');
            filter.fadeIn(300);
            filterBtn.addClass('active');   
            //btnBoxText.html(filterBtn.data('hide'));
            $('body').addClass('filter-open');
            filterOpen = true;
        }
    }

    $('body').on('click', '.open-filter', function(){
        filterOpen = false;
        openFilter();
    });

    $('body').on('click', '.close-filter', function(){
        if($(this).hasClass('reset-filter')) {
            $('.filter-post-list')[0].reset();
            $('.filter-post-list').change();
        }
        openFilter();
        return false;
    });

    $(window).on("load scroll", function () {
        if ($('#filterBtn').length > 0) {
            var scrollEl = $('#filterBtn').offset().top,
                scrollNav = $('.area-filter-show').offset().top + 100,
                navHeight = $('.area-filter-show').outerHeight();

            if (scrollEl + 100 > scrollNav && scrollEl < scrollNav + navHeight + 100) {
                setTimeout(function () {
                    $('#filterBtn').addClass('show');
                }, 50);
            }
            else {
                if(!filterOpen) {
                    setTimeout(function () {
                        $('#filterBtn').removeClass('show');
                    }, 50);
                }
            }
        }
    });


    // МНОГОУРОВНЕВЫЙ СПИСОК В СТРУКТУРЕ
    $('.structure-tree').dcAccordion({
        eventType: 'click',
        autoClose: false,
        saveState: false,
        disableLink: false,
        showCount: false,
        autoExpand: true,
        speed: 400,
    });


    // НАВИГАЦИЯ
    $('.nav-accordion').dcAccordion({
        eventType: 'click',
        autoClose: false,
        saveState: false,
        disableLink: false,
        showCount: false,
        autoExpand: true,
        speed: 400,
    });

    $('.structure-tree li.dcjq-current-parent > ul').slideDown();

    $(this).parents('.nav-tabs').find('.custom-tab-item.active').removeClass('active');
    $('.structure-tree ul').slideDown();
    $('.structure-tree .dcjq-parent-li .item-wrap').addClass('active');
    $(this).parent('li.custom-tab-item').addClass('active');

    // раскрыть все
    $('.structure-down').click(function () {
        $(this).parents('.nav-tabs').find('.custom-tab-item.active').removeClass('active');
        $('.structure-tree ul').slideDown();
        $('.structure-tree .dcjq-parent-li .item-wrap').addClass('active');
        $(this).parent('li.custom-tab-item').addClass('active');
        return false;
    });

    // раскрыть все
    $('.structure-up').click(function () {
        $(this).parents('.nav-tabs').find('.custom-tab-item.active').removeClass('active');
        $('.structure-tree ul').slideUp();
        $('.structure-tree .dcjq-parent-li .item-wrap').removeClass('active');
        $(this).parent('li.custom-tab-item').addClass('active');
        return false;
    });

    if ($('.scroll').length > 0) {
        $('.scroll').each(function () {
            var ps = new PerfectScrollbar($(this)[0]);
        });
    }

    // анимируем появление блоков
    if (device.desktop()) {
        // анимируем появление блоков
        $('.anim-block').addClass("anim-hidden").viewportChecker({
            classToAdd: 'anim-visible animated fadeInUp',
            offset: 200
        });
    }


    var matched, browser;

    jQuery.uaMatch = function (ua) {
        ua = ua.toLowerCase();

        var match = /(chrome)[ \/]([\w.]+)/.exec(ua) ||
            /(webkit)[ \/]([\w.]+)/.exec(ua) ||
            /(opera)(?:.*version|)[ \/]([\w.]+)/.exec(ua) ||
            /(msie) ([\w.]+)/.exec(ua) ||
            ua.indexOf("compatible") < 0 && /(mozilla)(?:.*? rv:([\w.]+)|)/.exec(ua) ||
            [];

        return {
            browser: match[1] || "",
            version: match[2] || "0"
        };
    };

    matched = jQuery.uaMatch(navigator.userAgent);
    browser = {};

    if (matched.browser) {
        browser[matched.browser] = true;
        browser.version = matched.version;
    }

    // Chrome is Webkit, but Webkit is also Safari.
    if (browser.chrome) {
        browser.webkit = true;
    } else if (browser.webkit) {
        browser.safari = true;
    }

    jQuery.browser = browser;


    if ($('.scroll').length > 0) {
        $('.scroll').each(function () {
            var ps = new PerfectScrollbar($(this)[0]);
        });
    }

    var $body = $('body');

    // СЛЛОИ В ШАПКЕ

    function bodyOverflowHidden() {
        setTimeout(function () {
            $body.css('overflow', 'hidden');
            if (device.desktop()) {
                if ($.browser.webkit || $.browser.mozilla) {
                    $('body').css('padding-right', '17px');
                }
            }
        }, 300);
    }

    function bodyOverflowAuto() {
        setTimeout(function () {
            $body.css('overflow', 'auto');
            if (device.desktop()) {
                if ($.browser.webkit || $.browser.mozilla) {
                    $('body').css('padding-right', '0');
                }
            }
        }, 300);
    }

    // закрытие слоя
    function closeLayers(layer, link) {
        layer.removeClass('open');
        $body.removeClass('layer-top-open');
        link.removeClass('act');
        $body.removeClass('open-panel-small');
        bodyOverflowAuto();
    }

    // открытие слоя
    function openLayer(layer, link) {
        if (layer.hasClass('panel-small')) {
            $body.addClass('open-panel-small');
            bodyOverflowAuto();
        }
        else {
            $body.removeClass('open-panel-small');
            bodyOverflowHidden();
        }
        $('.layer-top').removeClass('open');
        layer.addClass('open');
        $body.addClass('layer-top-open');
        $('.toggle-top-layer').removeClass('act');
        link.addClass('act');
        $body.removeClass('page-layer-open');
        $('.page-layer').removeClass('open');
        $('.open-page-layer').removeClass('act');
    }

    var pageOpen = false,
        header = $('.header');

    // слои сверху
    $('.toggle-top-layer').click(function () {
        var _this = $(this),
            id = _this.data('href'),
            layer = $('.layer-top[id="' + id + '"]');

        pageOpen = $body.hasClass('layer-top-open') ? true : false;

        if (!layer) {
            return false;
        }

        // если текущий слой уже открыт
        if (pageOpen == true && layer.hasClass('open')) {
            closeLayers(layer, _this);
        }
        // если открыт другой слой
        else if (pageOpen == true && $('.layer-top.open') > 0) {
            $body.addClass('anim-layers');
            openLayer(layer, _this);
            setTimeout(function () {
                $body.removeClass('anim-layers');
            }, 3000);
        }
        // если нет открытых слоев
        else {
            openLayer(layer, _this);
        }
    });

    $('.close-top-layer').click(function () {
        $('.layer-top').removeClass('open');
        $body.removeClass('layer-top-open');
        $('.toggle-top-layer').removeClass('act');
        $body.removeClass('open-panel-small');
        bodyOverflowAuto();
    });

    // end СЛЛОИ В ШАПКЕ

    $('.open-page-layer').click(function () {
        var _this = $(this),
            page = _this.data('href');
        if (_this.hasClass('act')) {
            $body.removeClass('page-layer-open');
            $('.page-layer').removeClass('open');
            _this.removeClass('act');
            bodyOverflowAuto();
            return false;
        }
        else {
            $body.addClass('page-layer-open');
            _this.addClass('act');
            $('.page-layer').not('[id="' + page + '"]').removeClass('open');
            $('.page-layer[id="' + page + '"]').addClass('open');
            closeLayers($('.layer-top'), $('.toggle-top-layer'));
            bodyOverflowHidden();
            return false;
        }
    });
    $('.close-page-layer').click(function () {
        $body.removeClass('page-layer-open');
        $('.page-layer').removeClass('open');
        $('.open-page-layer').removeClass('act');
        bodyOverflowAuto();
        return false;
    });


    // video audio play
    var $body = $('body');
    if ($('#section-media audio').length > 0) {
        $('#section-media audio').get(0).controls = false;
    }

    $body.on("click", '.video-audio-play', function () {
        var _this = $(this),
            video = _this.next('video').length > 0 ? _this.next('video').get(0) : false,
            audio = _this.next('audio').length > 0 ? _this.next('audio').get(0) : false,
            media = false;
        if (video != false) {
            media = video;
        }
        else if (audio != false) {
            media = audio;
        }
        else {
            return false;
        }
        if (media) {
            if (media.paused) {
                $('.video-preview').fadeOut(300);
                $('.video-title').fadeOut(300);
                media.play();
                media.controls = true;
                _this.addClass("paused");
                $('.wrap-media-video').addClass('play');
            }
            else {
                $('.video-preview').fadeIn(300);
                $('.video-title').fadeIn(300);
                media.pause();
                media.controls = false;
                _this.removeClass("paused");
                $('.wrap-media-video').removeClass('play');
            }
        }
    });

    $(document).on('ready', function () {
        if (typeof($.fancybox) !== 'undefined') {
            jQuery.fancybox.defaults.baseTpl =
                '<div class="media-photo-modal fancybox-container" role="dialog" tabindex="-1">' +
                '<div class="fancybox-bg"></div>' +
                '<div class="fancybox-inner">' +
                '<div class="fancybox-navigation">{{arrows}}</div>' +
                '<div class="fancybox-stage"></div>' +
                '<div class="fancybox-caption-wrap">' +
                '<div class="fancybox-infobar">' +
                '<span data-fancybox-index></span>&nbsp;/&nbsp;<span data-fancybox-count></span>' +
                '</div>' +
                '<div class="fancybox-caption"></div>' +
                '<div class="date"></div>' +
                '</div>' +
                '<div class="fancybox-toolbar">{{buttons}}</div>' +
                '</div>' +
                '</div>';
            jQuery.fancybox.defaults.idleTime = false;
            jQuery.fancybox.defaults.baseClass = 'fancybox-custom-layout';
            jQuery.fancybox.defaults.margin = 0;
            jQuery.fancybox.defaults.gutter = 0;
            jQuery.fancybox.defaults.infobar = true;
            jQuery.fancybox.defaults.touch = {
                vertical: false
            };
            jQuery.fancybox.defaults.buttons = [
                'close'
            ];
            jQuery.fancybox.defaults.animationEffect = "fade";
            jQuery.fancybox.defaults.animationDuration = 500;
            jQuery.fancybox.defaults.onInit = function (instance) {
                // Create new wrapping element, it is useful for styling
                // and makes easier to position thumbnails
                instance.$refs.inner.wrap('<div class="fancybox-outer"></div>');
            }
        }

        $("a.fancybox").fancybox({
            tpl: {
                next: '<a title="Вперед" class="fancybox-nav fancybox-next"><span></span></a>',
                prev: '<a title="Назад" class="fancybox-nav fancybox-prev"><span></span></a>',
                closeBtn : '<a title="Закрыть" class="fancybox-item fancybox-close" href="javascript:;"></a>',
            }
        });

    });

    // pagination
    $('.disabled a').on('click', function (e) {
        e.preventDefault();
    });

    var breadcrumb = $('.breadcrumb');

    $('body').on('click', '.wrap-pagination li:not(.disabled) a', function () {
        $('body, html').animate({
            scrollTop: breadcrumb.length > 0 ? breadcrumb.offset().top + "px" : 0
        }, 700);
    });

    // обертка для таблиц в контент-зоне
    $('.text-block table').each(function () {
        $(this).wrapAll('<div class="table-wrapper"></div>');
    });

    // таблицы переносим в модальное окно
    if ($('.table-modal').length) {
        function tableModal(table, id, btn, title) {
            var tableModalWrap = '<div id="' + id + '" class="modal fade modal-wide" role="dialog">' +
                '<div class="modal-dialog">' +
                '<div class="modal-content">' +
                '<div class="modal-header">' +
                '<button type="button" class="close" data-dismiss="modal">&times;</button>' +
                '<h4 class="modal-title">' + title + '</h4>' +
                '</div>' +
                '<div class="modal-body">' +
                '</div>' +
                '</div>' +
                '</div>' +
                '</div>';

            table.after('<span class="btn btn-block btn-primary mr-bottom-30 btn-wrap-normal" data-toggle="modal" data-target="#' + id + '">' + btn + '</span>');
            $('body').append(tableModalWrap);
            table.addClass('table-style table').appendTo('body #' + id + ' .modal-body');

        }

        $('.table-modal').not('.table-no-modal').each(function (i, el) {
            var $this = $(this),
                btn = $this.attr('data-btn') !== undefined && $this.attr('data-btn') !== false && $this.data('data-btn') !== '' ? $this.data('btn') : 'Таблица: Нажмите для просмотра',
                title = $this.attr('data-title') !== undefined && $this.attr('data-title') !== false && $this.data('data-title') !== '' ? $this.data('title') : '',
                id = 'modalTable_' + i;
            tableModal($this, id, btn, title);
        });
    }

    $('.field-icon-loupe').focus(function () {
        $(this).addClass('full');
    }).blur(function () {
        var count = $(this).val().length;
        if (count === 0) {
            $(this).removeClass('full');
        }
        else {
            $(this).addClass('full');
        }
    });


    // form date input
    if ($(".date-wiget").length > 0) {
        $(window).on('resize load', function () {
            $(".date-wiget").each(function () {
                var $this = $(this);
                $this.find('.date-start').Zebra_DatePicker({
                    view: 'years',
                    direction: false,
                    pair: $this.find('.date-end'),
                    open_icon_only: true,
                    readonly_element: false,
                    format: "d/m/Y",
                    show_clear_date: true,
                    onClose: function() {
                        $('.date-start').trigger('change');
                    }
                });
                $this.find('.date-end').Zebra_DatePicker({
                    view: 'years',
                    direction: 1,
                    open_icon_only: true,
                    readonly_element: false,
                    format: "d/m/Y",
                    show_clear_date: true,
                    onClose: function() {
                        $('.date-end').trigger('change');
                    }
                });
            });
            $('#date-year').Zebra_DatePicker({
                open_icon_only: true,
                direction: false,
                readonly_element: false,
                format: "Y",
                view: 'years',
                show_clear_date: true,
                onClose: function() {
                    $('#date-year').trigger('change');
                }
            })
        });
    }


    // spoiler
    $('.spoiler-box__btn').click(function(){
        var parent = $(this).closest('.spoiler-box'),
            content = $(this).next('.spoiler-box__content');
        if(parent.hasClass('open')){
            parent.removeClass('open');
            content.slideUp(300); 
        }
        else{
            parent.addClass('open');
            content.slideDown(300);
        }
        return false;
    });

    if($('.spoiler-box').length) {
        var url = window.location.href,
            id = url.indexOf("#") + 1 != 0 ? url.substring(url.indexOf("#") + 1) : false,
            activeSpoiler,
            child = false;
        if(id) {
            if($('.spoiler-box[id="'+id+'"]').length) {
                activeSpoiler = $('.spoiler-box[id="'+id+'"]');
                activeSpoiler.find('.spoiler-box__btn').click();
                setTimeout(function(){
                    $(window).scrollTo(activeSpoiler);
                }, 500);
            }
            else if ($('#'+id).closest('.spoiler-box').length) {
                child = $('#'+id);
                activeSpoiler = child.closest('.spoiler-box');
                activeSpoiler.find('.spoiler-box__btn').click();
                setTimeout(function(){
                    $(window).scrollTo(child);
                }, 500);
            }
            else {
                activeSpoiler = false;
            }
        }
    }

    // функция для фиксации плавающих блоки в сайдбарах
    function widthFixBlockAside(elem, elemParent) {
        elem.css({
            'width': elemParent.width()
        });
    }


    // show-more-bottom

    var mobile = (window.matchMedia('(max-width: 767px)').matches) ? true : false;

    function showMoreFunction(){
        if($('.show-more-bottom').length > 0) {
            $('.show-more-bottom .tab-pane').each(function(){
                var $this = $(this),
                    amount = mobile ? $this.data('amount-mobile') : $this.data('amount'),
                    parent = $this.closest('.show-more-bottom'),
                    btn = parent.find('.show-more-bottom-link');
                
                if($this.hasClass('active')){
                    if ($this.find('.more-bottom-box').length <= amount){
                        btn.hide();
                    }
                    else {
                        btn.show();
                    }
                }
                $this.find('.more-bottom-box:gt('+(amount-1)+')').hide();
            });
        }
    }

    $(window).on("load resize", function() {
        showMoreFunction();
    });

    $('.show-more-bottom-link').on('click', function(){
        var $this = $(this),
            parent = $this.closest('.show-more-bottom'),
            amount = mobile ? parent.find('.tab-pane.active').data('amount-mobile') : parent.find('.tab-pane.active').data('amount'),
            activeBoxesHide = parent.find('.tab-pane.active .more-bottom-box:gt('+(amount-1)+')');
        if ($this.hasClass('open')) {
            $this.removeClass('open').find('span').html('Показать больше');
            activeBoxesHide.fadeOut(300);
        }
        else {
            $this.addClass('open').find('span').html('Скрыть');
            activeBoxesHide.fadeIn(300);
        }
        return false;
    });

    $('.show-more-bottom a[data-toggle="tab"]').on('show.bs.tab', function (e) {
        var $this = $(this),
            parent = $this.closest('.show-more-bottom'),
            tab =  $(e.target),
            tab = $(tab.attr('href')),
            btn = parent.find('.show-more-bottom-link'),
            amount = mobile ? tab.data('amount-mobile') : tab.data('amount');
        btn.removeClass('open').find('span').html('Показать больше');
        parent.find('.tab-pane').each(function () {
            $(this).find('.more-bottom-box:gt('+(amount-1)+')').hide();
        });
        if(tab.find('.more-bottom-box').length <= amount){
            btn.hide();
        }
        else {
            btn.show();
        }
    });

    // end show-more-bottom

    // form placeholder fix

    $('.form-group--placeholder-fix').on('focus', 'textarea, input:not(:hidden)', function () {
        $(this).closest('.form-group--placeholder-fix').addClass('full');
    }).on('blur', 'textarea, input:not(:hidden)', function () {
        var count = $(this).val().length;
        if (count === 0) {
            $(this).closest('.form-group--placeholder-fix').removeClass('full');
        }
    });
    
    $('.form-group--placeholder-fix').on('click', '.placeholder', function() {
        $(this).next('input').focus();
        $(this).next('span').find('input').focus();
        $(this).next('textarea').focus();
        $(this).next('span').find('textarea').focus();
    });

    $(document).ready(function () {
      $('.form-group--placeholder-fix input:not(:hidden), .form-group--placeholder-fix textarea').each(function () {
          var count = $(this).val().length;
          if (count != 0) {
              $(this).closest('.form-group--placeholder-fix').addClass('full');
          }
      });
    });

    // end form placeholder fix


    // form el counter

    $(".form-el-show-counter textarea").bind('textchange', function () {
        formCounter($(this));
    });
    $(".form-el-show-counter input:not(:hidden)").on('input keyup', function () {
        formCounter($(this));
    });
    $(".form-el-show-counter").each(function(index, el) {
        var $this = $(this);
            formEl = $this.find('input:not(:hidden)').length ? $this.find('input:not(:hidden)') : $this.find('textarea');
        if(formEl) {
            var maxlength = formEl.attr('maxlength');
            $this.find('.maxlength').html(maxlength);
            $this.find('.remain').html(maxlength);
        }
        else {
            $this.find('.form-el-counter').hide();
        }
    });
    function formCounter($el){
        var count = $el.val().length,
            countBox = $el.closest('.form-el-show-counter').find('.form-el-counter').length ? $el.closest('.form-el-show-counter').find('.form-el-counter') : false;
        if(countBox){
            if (count > 0) {
                // countBox.show();
                countBox.find('.remain').html($el.attr('maxlength') - count);
            }
            else {
                countBox.hide();
            }
        }
    }

    // end form el counter

    if ($('#sliderMaterials').length > 0) {
        $('#sliderMaterials .slider').slick({
            autoplay: false,
            autoplaySpeed: 2500,
            dots: false,
            infinite: true,
            slidesToShow: 1,
            arrows: true,
            prevArrow: '.slider-materials-nav .slider-vert__nav-prev',
            nextArrow: '.slider-materials-nav .slider-vert__nav-next',
        });
    }

    if ($('#sliderDoc').length > 0) {
        $('#sliderDoc .slider').slick({
            autoplay: false,
            autoplaySpeed: 2500,
            dots: false,
            infinite: true,
            slidesToShow: 1,
            arrows: true,
            prevArrow: '.slider-doc-nav .slider-vert__nav-prev',
            nextArrow: '.slider-doc-nav .slider-vert__nav-next',
        });
    }

    $('input[type=checkbox], input[type=radio], input[type=file]').styler();

    // функция для фиксации плавающих блоков в сайдбаре
    function fixBlockAside(elem, elemParent, placeFix, indent) {
        if (elemParent.length <= 0) {
            return false;
        }
        if ($(window).scrollTop() <= elemParent.offset().top - indent) {
            elem.css({
                'top': 0
            }).removeClass('fix');
        }
        else if ($(window).scrollTop() > placeFix.height() - elem.height() - indent) {
            elem.css({
                'top': placeFix.height() - elem.height() - elemParent.offset().top
            }).removeClass('fix');
        }
        else {
            elem.css({
                'top': indent
            }).addClass('fix');
        }
    }

    if ($('.fix-block-aside').length > 0) {
        widthFixBlockAside($('.fix-block-aside'), $('.wrap-aside-fix'));
        fixBlockAside($('.fix-block-aside'), $('.wrap-aside-fix'), $('.main'), 70);

        $(window).on('scroll', function () {
            fixBlockAside($('.fix-block-aside'), $('.wrap-aside-fix'), $('.main'), 70);
        });

        $(window).on('resize', function () {
            widthFixBlockAside($('.fix-block-aside'), $('.wrap-aside-fix'));
            fixBlockAside($('.fix-block-aside'), $('.wrap-aside-fix'), $('.main'), 70);
        });
    }

    // toggle
    $('.toggle-container .trigger').click(function () {
        var $this = $(this),
            active = $this.hasClass('active'),
            $box = $this.closest('.toggle-container').find('.toggle-container__more');
        $box
            .toggleClass('expanded')
            .slideToggle(500);
        $this
            .toggleClass('active')
            .text(active ? 'Читать далее' : 'Свернуть');
        return false;
    });

    // link-animate-scroll
    $("a.link-animate-scroll").click(function () {
        var elementClick = $(this).attr("href");
        var destination = $(elementClick).offset().top;
        jQuery("html:not(:animated),body:not(:animated)").animate({
            scrollTop: destination
        }, 800);
        return false;
    });

    $('.open-modal-blind').on('click', function () {
        var layuer = $('#panelBlind');
        var link = $('.header__blind-btn span');
        openLayer(layuer, link);
    });

    $('.close-modal').on('click', function (e) {
        e.preventDefault();
        modalWrap.removeClass('active');
        $(this).parent().removeClass('active');
    });

    // blind mode

    $('.btn-garniture').on('click', function (e) {
        e.preventDefault();
        var garniture = $(this).attr('data-class');
        $('.btn-garniture').removeClass('active');
        $(this).addClass('active');
        $('html').attr('garniture', garniture).trigger('blind.set.garniture', [garniture]);
    });

    $('.btn-kerning').on('click', function (e) {
        e.preventDefault();
        var kerning = $(this).attr('data-class');
        $('.btn-kerning').removeClass('active');
        $(this).addClass('active');
        $('html').attr('kerning', kerning).trigger('blind.set.kerning', [kerning]);
        setTimeout(function () {
            initNavComponent();
            initHeaderNav();
        }, 200);
    });

    $('.btn-font').on('click', function (e) {
        e.preventDefault();
        var fontSize = $(this).attr('data-class');
        $('.btn-font').removeClass('active');
        $(this).addClass('active');
        $('html').attr('font-size', fontSize).trigger('blind.set.fontSize', [fontSize]);
        setTimeout(function () {
            initNavComponent();
            initHeaderNav();
        }, 200);
    });

    $('.btn-color').on('click', function (e) {
        e.preventDefault();
        var colorSchema = $(this).attr('data-class');
        $('.btn-color').removeClass('active');
        $(this).addClass('active');
        $('html').attr('color-schema', colorSchema).trigger('blind.set.colorSchema', [colorSchema]);
    });

    $('.btn-img').on('click', function (e) {
        e.preventDefault();
        var imgDisplay = $(this).attr('data-img');
        $('.btn-img').removeClass('active');
        $(this).addClass('active');
        $('html').attr('img-display', imgDisplay).trigger('blind.set.imgDisplay', [imgDisplay]);
    });


    // возврат к дефолтным настройкам
    $('.default-site-version').click(function () {
        $('html').attr('font-size', 'size-sm').trigger('blind.unset.fontSize', ['size-sm']);
        $('html').attr('color-schema', 'color-white').trigger('blind.unset.colorSchema', ['color-white']);
        $('html').attr('img-display', 'show').trigger('blind.unset.imgDisplay', ['img-show']);
        $('html').attr('kerning', 'size-sm').trigger('blind.unset.kerning', ['size-sm']);
        $('html').attr('garniture', 'sans-serif').trigger('blind.unset.garniture', ['sans-serif']);
        $('.btn-color').removeClass('active');
        $('.btn-color.color-white').addClass('active');
        $('.btn-font').removeClass('active');
        $('.btn-font.size-sm').addClass('active');
        $('.btn-img').removeClass('active');
        $('.btn-img.img-show').addClass('active');
        $('.btn-kerning').removeClass('active');
        $('.btn-kerning.size-sm').removeClass('active');
        $('.btn-garniture').removeClass('active');
        $('.btn-garniture.sans-serif').addClass('active');
        setTimeout(function () {
            initNavComponent();
            initHeaderNav();
        }, 200);
        return false;
    });

    // datepicker
    if ($("#tempust").length > 0) {
        $("#tempust").tempust({
            date: new Date(),
            offset: 1,
            events: {
                "2017/6/1": $("<div><p class='ev-date'>30 - 31 мая, Москва</p><p class='ev-text'>Финал V Международного инженерного чемпионата «Case-in»</p></div>"),
                "2017/6/3": $("<div><p class='ev-date'>30 - 31 мая, Москва</p><p class='ev-text'>Финал V Международного инженерного чемпионата «Case-in»</p></div>")
            }
        });
    }

    // galleria
    if ($("#galleria").length > 0) {

        Galleria.addTheme({
            name: 'classic',
            version: 1.5,
            author: 'Galleria',
            defaults: {
                transition: 'slide',
                thumbCrop: 'height',

                // set this to false if you want to show the caption all the time:
                _toggleInfo: false
            },
            init: function (options) {

                Galleria.requires(1.4, 'This version of Classic theme requires Galleria 1.4 or later');

                // add some elements
                this.addElement('info-link', 'info-close');
                this.append({
                    'info': ['info-link', 'info-close']
                });

                this.addElement('btn-screen');
                this.addElement('download');

                this.appendChild('counter', 'btn-screen');
                this.appendChild('container', 'download');

                // cache some stuff
                var info = this.$('info-link,info-close,info-text'),
                    touch = Galleria.TOUCH;

                // show loader with opacity
                this.$('loader').show().css('opacity', 0.4);

                // some stuff for non-touch browsers
                if (!touch) {
                    this.addIdleState(this.get('image-nav-left'), {left: -50});
                    this.addIdleState(this.get('image-nav-right'), {right: -50});
                    this.addIdleState(this.get('counter'), {top: -50});
                    this.addIdleState(this.get('download'), {top: -50});
                }

                // toggle info
                if (options._toggleInfo === true) {
                    info.bind('click:fast', function () {
                        info.toggle();
                    });
                } else {
                    info.show();
                    this.$('info-link, info-close').hide();
                }

                // bind some stuff
                this.bind('thumbnail', function (e) {

                    if (!touch) {
                        // fade thumbnails
                        $(e.thumbTarget).css('opacity', 0.6).parent().hover(function () {
                            $(this).not('.active').children().stop().fadeTo(100, 1);
                        }, function () {
                            $(this).not('.active').children().stop().fadeTo(400, 0.6);
                        });

                        if (e.index === this.getIndex()) {
                            $(e.thumbTarget).css('opacity', 1);
                        }
                    } else {
                        $(e.thumbTarget).css('opacity', this.getIndex() ? 1 : 0.6).bind('click:fast', function () {
                            $(this).css('opacity', 1).parent().siblings().children().css('opacity', 0.6);
                        });
                    }
                });

                var activate = function (e) {
                    $(e.thumbTarget).css('opacity', 1).parent().siblings().children().css('opacity', 0.6);
                };

                this.bind('loadstart', function (e) {
                    if (!e.cached) {
                        this.$('loader').show().fadeTo(200, 0.4);
                    }
                    window.setTimeout(function () {
                        activate(e);
                    }, touch ? 300 : 0);
                    this.$('info').toggle(this.hasInfo());
                });

                this.bind('loadfinish', function (e) {
                    this.$('loader').fadeOut(200);
                });
            }
        });

        Galleria.run('#galleria', {
            imageCrop: true,
            thumbnails: false,
            transition: 'fade',
            trueFullscreen: true
        });

        Galleria.ready(function () {
            $('.galleria-theme-classic .galleria-btn-screen').on('click', function () {
                $(this).toggleClass('sl-fullscreen');
                $('#galleria').data('galleria').toggleFullscreen();
            });

            var download = document.createElement('a');
            download.className = 'link-download';
            download.setAttribute('download', 'download');
            $('.galleria-download').append(download);

            this.bind('image', function (e) {
                download.setAttribute('href', e.imageTarget.getAttribute('src'));
            });
        });
    }


    // Old script
    function setEqualHeight($els) {
        var maxHeight = 0;
        $.each($els, function (i, item) {
            var elHeight = $(item).height();
            if (elHeight > maxHeight) {
                maxHeight = elHeight;
            }
        });
        $.each($els, function (i, item) {
            $(item).height(maxHeight);
        });
    }

    // hiding beta block
    $('.beta-close a').on('click', function () {
        $(this).closest('.beta-version').addClass('hide');
    });

    // Custom tabs
    function customTabs(navId, contentId) {
        var $navEl = $('#' + navId);
        var $navItems = $navEl.find('.custom-tab-item');
        var $contentEl = $('#' + contentId);
        var $contentItems = $contentEl.find('.custom-tabs-content');


        $navItems.on('click', function (event) {
            var $selectedTab = $(this);
            $navItems.removeClass('active');
            $selectedTab.addClass('active');
            $contentItems.fadeOut(0).removeClass('active');
            $contentEl.find('#' + $selectedTab.data('content')).stop().fadeIn(300).addClass('active');
        });
    }

    customTabs('day_map_tabs_nav', 'day_map_tabs_content');
    customTabs('media_tabs_nav', 'media_tabs_content');

    $("[data-toggle=popover]").popover({
        html: true,
        content: function () {
            var content = $(this).attr("data-popover-content");
            return $(content).children(".popover-body").html();
        },
        title: function () {
            var title = $(this).attr("data-popover-content");
            return $(title).children(".popover-heading").html();
        },
        delay: 150,
    }).on('shown.bs.popover', function (e) {
        var popover = $(this);
        $(this).parent().find('.close').on('click', function (e) {
            popover.popover('hide');
        });
    });

    $("[data-toggle=popover-body]").popover({
        html: true,
        content: function () {
            var content = $(this).attr("data-popover-content");
            return $(content).children(".popover-body").html();
        },
        title: function () {
            var title = $(this).attr("data-popover-content");
            return $(title).children(".popover-heading").html();
        },
        container: 'body',
        delay: 150,
    }).on('shown.bs.popover', function (e) {
        var popover = $(this);
        $(this).parent().find('.close').on('click', function (e) {
            popover.popover('hide');
        });
    });


    // услуги на главной показать больше

    if ($('#sectionServices').length > 0) {
        $('#sectionServices .tab-pane').each(function () {
            var $this = $(this),
                more = $this.find('.services-more-btn')
            if ($this.find('.services-box').length > 3) {
                $this.find('.services-box:gt(2)').hide();
            }
            else {
                more.hide();
            }
        });
    }

    $('.services-more-btn').click(function () {
        var $this = $(this),
            tab = $this.closest('.tab-pane'),
            boxesHide = tab.find('.services-box:gt(2)');

        if ($this.hasClass('open')) {
            $this.removeClass('open').find('span').html($this.data('open'));
            boxesHide.fadeOut(300);
        }
        else {
            $this.addClass('open').find('span').html($this.data('hide'));
            boxesHide.fadeIn(300);
        }
        return false;
    });

    $('#navbar-uslugi a[data-toggle="tab"]').on('show.bs.tab', function (e) {
        $('.services-more-btn').each(function () {
            $(this).removeClass('open').find('span').html($(this).data('open'));
        });
        $('#sectionServices .tab-pane').each(function () {
            $(this).find('.services-box:gt(2)').hide();
        });
    });


    $('#navbar-uslugi a[data-toggle="tab"]').on('show.bs.tab', function (e) {
        $('#servicesMoreBtn').removeClass('open').find('span').html('Показать больше');
        $('#sectionServices .tab-pane').each(function () {
            $(this).find('.services-box:gt(2)').hide();
        });
    });

    // если два блока подряд идут с цветным бг, добавляем класс (меняются отступы)
    $('.main .section').each(function () {
        var $this = $(this);
        if ($this.hasClass('section--bg') && $this.next('.section').hasClass('section--bg')) {
            $this.addClass('stuck first');
            $this.next('.section').addClass('stuck last');
        }
    });

    // dropdown navbar в шапке
    $('.li-static').mouseenter(function () {
        if ($(window).innerWidth() > 768) {
            $(this).find('.nav-submenu').stop().fadeIn(200);
        }
    });

    $('.li-static').mouseleave(function () {
        if ($(window).innerWidth() > 768) {
            $(this).find('.nav-submenu').stop().fadeOut(200);
        }
    });


    // dep-open-card

    $('.dep-open-card__heading').click(function (e) {
        e.preventDefault();

        $(this).parent().toggleClass('active');
    });

})();

(function ($) {


    var nowDate = new Date(),
        slickSlidesToShow,
        nowDateIndexPosition,
        slickSlidesToScroll = 3,
        $prevBtn = $('#main-calendar-widget .calendar--prev-arrow'),
        $nextBtn = $('#main-calendar-widget .calendar--next-arrow');

    $('.custom-tab-item--calendar').on('click', function () {
        slickCalendar();
    });

    function slickCalendar() {

        // переменные и константы
        var $calendar = $('#main-calendar-widget'),
            $eventContainer = $('.event-container'),
            $eventElems = $eventContainer.find('.event'),
            $calendarCounter = 0,
            CALENDAR_HEADING_HEIGHT = 80,
            $curDateBtn = $calendar.find('.calendar__current_date'),
            $calendarContent = $calendar.find('.calendar-content'),
            $calendarSelectYear = $('select#calendar-select-year'),
            $calendarSelectMonth = $('select#calendar-select-month');

        $('#main-calendar-widget .calendar-content').slick({
            slidesToShow: 13,
            touchThreshold: 13,
            slidesToScroll: slickSlidesToScroll,
            infinite: false,
            prevArrow: $prevBtn,
            nextArrow: $nextBtn
        });


        setTimeout(function () {
            $('#main-calendar-widget').addClass('active');

        }, 1000);


        var calendarEvents = {
            loadMonth: function (year) {

                $.ajax({
                    url: $calendarSelectMonth.data('url'),
                    data: {'year': year},
                    dataType: 'JSON',
                    method: 'GET',
                    success: function (data) {
                        if (data.success) {
                            $calendarSelectMonth.empty();
                            for (var i in data.options) {
                                if (!data.options.hasOwnProperty(i)) {
                                    continue;
                                }
                                var option = data.options[i];
                                $calendarSelectMonth
                                    .append('<option value="' + i + '" data-subtext="' + option.events +
                                        '">' + option.title + '</option>');
                            }

                            if ($('.day.has-event[data-year=' + year + ']').length > 0) {
                                var $day = $('.day.has-event[data-year=' + year + ']:first'),
                                    month = $day.data('month'),
                                    goToElem = $day.index() - (Math.floor(slickSlidesToShow / 2));
                                console.log('index: ', goToElem, year, month);
                                calendarEvents.setSelects(year, month);
                                $calendarContent.slick('slickSetOption', 'slidesToScroll', 1)
                                    .slick('slickGoTo', goToElem)
                                    .slick('slickSetOption', 'slidesToScroll', slickSlidesToScroll);
                            }

                            $calendarSelectMonth.selectpicker('refresh');
                        }
                    }
                });
            },
            // Врубаем селекты
            setSelects: function (year, month) {
                if (year) {
                    var oldYear = $calendarSelectYear.find('option:selected').val();
                    if (oldYear !== year) {
                        this.loadMonth(year);
                    }
                    $calendarSelectYear.find('option[value=' + year + ']').prop('selected', true);
                }
                if (month) {
                    $calendarSelectMonth.find('option[value=' + month + ']').prop('selected', true);
                }
                $calendarSelectYear.selectpicker('refresh');
                $calendarSelectMonth.selectpicker('refresh');
            },
            // Выбираем год
            nextYear: function (activeYear) {
                this.loadMonth(activeYear);
            },
            // Выбираем месяц
            nextMonth: function (activeYear, activeMonth) {
                var goToElem = 0;
                if ($('.day.has-event[data-year=' + activeYear + '][data-month=' + activeMonth + ']').length > 0) {
                    goToElem = $('.day.has-event[data-year=' + activeYear + '][data-month=' + activeMonth + ']:first').index()
                        - (Math.floor(slickSlidesToShow / 2));

                    $calendarContent.slick('slickSetOption', 'slidesToScroll', 1)
                        .slick('slickGoTo', goToElem)
                        .slick('slickSetOption', 'slidesToScroll', slickSlidesToScroll);
                    return true;
                }
                var $firstDayOfMonth = $('.day.first[data-year=' + activeYear + '][data-month=' + activeMonth + ']');
                if ($firstDayOfMonth.length > 0) {
                    goToElem = $firstDayOfMonth.index();
                    $calendarContent.slick('slickSetOption', 'slidesToScroll', 1)
                        .slick('slickGoTo', goToElem)
                        .slick('slickSetOption', 'slidesToScroll', slickSlidesToScroll);
                }
            }
        };

        slickSlidesToShow = $calendarContent.slick('slickGetOption', 'slidesToShow');
        // slickSlidesToScroll = $calendarContent.slick('slickGetOption', 'slidesToScroll');


        nowDateIndexPosition = $calendarContent.find('.day.active').index() - (Math.floor(slickSlidesToShow / 2));


        $calendarContent.slick('slickGoTo', nowDateIndexPosition);

        calendarEvents
            .setSelects($calendarContent.find('.day.active').attr('data-year'),
                $calendarContent.find('.day.active').attr('data-month'));

        $calendarContent.slick('slickSetOption', 'slidesToScroll', 3);

        $curDateBtn.on('click', function (e) {
            e.preventDefault();
            $calendarContent.slick('slickGoTo', nowDateIndexPosition);
            calendarEvents
                .setSelects($calendarContent.find('.day.active').attr('data-year'),
                    $calendarContent.find('.day.active').attr('data-month'));
        });

        $calendarSelectYear.on('change', function () {
            var activeYear = $(this).val(),
                activeMonth = $calendarSelectMonth.val();

            calendarEvents.nextYear(activeYear, activeMonth);
        });


        $calendarSelectMonth.on('change', function () {
            var activeYear = $calendarSelectYear.val(),
                activeMonth = $(this).val();


            calendarEvents.nextMonth(activeYear, activeMonth);
        });


        $nextBtn.on('click', function () {
            for (var i = 0; i < $('.day.first').length; i++) {
                var elem = $('.day.first').eq(i);
                if (elem.hasClass('slick-active')) {
                    calendarEvents.setSelects(elem.attr('data-year'), elem.attr('data-month'));
                    break;
                }
            }
            $('.slick-active [data-toggle="popover"]').popover();
        });


        $prevBtn.on('click', function () {
            for (var i = 0; i < $('.day.last').length; i++) {
                var elem = $('.day.last').eq(i);
                if (elem.hasClass('slick-active')) {
                    calendarEvents.setSelects(elem.attr('data-year'), elem.attr('data-month'));
                    break;
                }
            }
            $('.slick-active [data-toggle="popover"]').popover();
        });


        $calendarContent.find('.day.has-event .day-content').on('click', function (e) {
            e.preventDefault();
            var elem = $(this).parent();
            $calendarCounter = 0;

            // Прячем все события
            $eventContainer
                .stop()
                .removeClass('active')
                .fadeOut(0);

            $eventElems
                .stop()
                .removeClass('active first')
                .fadeOut(0);

            // Показываем события нужного дня
            $eventContainer
                .find('.event[data-date=' + elem.attr('data-date') + ']')
                .each(function () {
                    console.log($(this).index());
                    if ($calendarCounter === 0) {
                        $(this).addClass('first');
                    }
                    $(this).stop().addClass('active').fadeIn(200);
                    $calendarCounter++;
                });

            // показываем блок с событиями
            $eventContainer
                .fadeIn(200)
                .addClass('active');

            // изменяем высоту календаря
            if ($calendar.outerHeight() < $eventContainer.outerHeight()) {
                $calendar
                    .css('height',
                        $eventContainer.outerHeight() +
                        CALENDAR_HEADING_HEIGHT + 'px');
            }
        });


        $('.event-container .event .event-close').click(function () {
            var $eventContainer = $('.event-container'),
                $eventElems = $eventContainer.find('.event'),
                $calendar = $('#main-calendar-widget');

            // обнуляем счетчик
            $calendarCounter = 0;

            $eventContainer
                .stop()
                .fadeOut(200)
                .removeClass('active');

            $eventElems
                .fadeOut(0)
                .removeClass('active first');

            $calendar
                .css('height', '');
        });


        var newEventIndex = $calendarContent.find('.day.active')
            .next('.day.has-event').index();

        $('.btn-calendar').on('click', function (e) {
            e.preventDefault();

            $calendarContent.slick('slickSetOption', 'slidesToScroll', 1);

            if (newEventIndex < $('.day.has-event').length - 1 && newEventIndex >= 0) {
                newEventIndex += 1;
            } else {
                newEventIndex = 0;
            }


            $calendarContent.slick(
                'slickGoTo',
                $('.day.has-event').eq(newEventIndex).index() + 1 -
                ($('.day.slick-active').length / 2));

            $calendarContent.slick('slickSetOption', 'slidesToScroll', 3);
        })
    }

})(jQuery);
