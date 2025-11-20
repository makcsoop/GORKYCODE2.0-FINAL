$('.select-search').on('click', function () {

    $('.select-search').removeClass('active');
    var module = $(this).data('module');
    $('.select-search').filter('[data-module="' + module + '"]').addClass('active');
    $('.hidden-module').val(module);

    return false;
});

$('#navbar-search .custom-tab-item a').on('click', function (event) {

        var $this = event.target,
            $url = $($this).attr('href');

        $('#navbar-search .custom-tab-item').removeClass('active');
        $($this).parent('.custom-tab-item').addClass('active');

        $.ajax({
            type: 'get',
            url: $url,
            dataType: "html",
            success: function (result) {
                $('.search-result').empty().html(result);
            }
        });

        return false;
    }
);

$('.search-result').on('click', '.custom-pagination a', function (event) {
    var $this = event.target;
    if (!$($this).parent('li').hasClass('disabled')) {
        return loadSearch(event);
    }
    }
);

$('.search-result').on('click', '#searchPageByPage', function (event) {
        return loadSearch(event);
    }
);

$('.search-result').on('click', '#searchShowMore', function (event) {

        var $url = $(event.target).attr('href');
        var id = $(event.target).closest('.search-more-result').attr('id');

        $.ajax({
            type: 'get',
            url: $url,
            dataType: "html",
            success: function (result) {
                $('#' + id).empty().html(result);
            }
        });

        return false;
    }
);


$('.param-search').click(function () {
    var $this = $(this),
        param = $('.param-search-toggle');
    if ($this.hasClass('active')) {
        $this.removeClass('active');
        param.slideUp(300).removeClass('open');
    }
    else {
        $this.addClass('active');
        param.slideDown(300);
    }
});

function loadSearch(event) {

    var $url = $(event.target).attr('href');

    $.ajax({
        type: 'get',
        url: $url,
        dataType: "html",
        success: function (result) {
            $('.search-result').empty().html(result);
        }
    });

    var offsetTop = $('#navbar-search').offset().top;
    $('html, body').animate({scrollTop: offsetTop}, 500);

    return false;
}
