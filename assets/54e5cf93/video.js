// Load the IFrame Player API code asynchronously.
/*var tag = document.createElement('script');
tag.src = "https://www.youtube.com/player_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;
var yt_container = $('#youtube');

function onYouTubePlayerAPIReady() {
    player = new YT.Player('youtube', {        
        videoId: yt_container.data('code'),
        playerVars: {
            controls: 0,
            showinfo: 0,
            rel: 0,
            autoplay: 0,
        },
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange,
        }
    });
}

function onPlayerReady(event) 
{
    yt_container.contents().find('.ytp-cued-thumbnail-overlay').hide();
    document.getElementById('video-play').addEventListener('click', function() {
        $('.video-preview').fadeOut(300);
        $('.video-title').fadeOut(300);
        $(this).hide();            
        player.playVideo();
    });
}

function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.PAUSED) {
        $('.video-preview').fadeIn(300);
        $('.video-title').fadeIn(300);
        $('#video-play').show();
    }
}*/

var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// youtube
var player,
    $ytСontainer = $('#youtube'),
    $ytWrap = $('#ytWrap'),
    ytPreview = document.getElementById('ytPreview'),
    ytPlay = document.getElementById('ytPlay');
    ytTitle = document.getElementById('ytTitle');


function onYouTubePlayerAPIReady() {
    player = new YT.Player('youtube', {        
        videoId: $ytСontainer.data('code'),
        playerVars: {
            controls: 1,
            showinfo: 0,
            rel: 0,
            autoplay: 0,
        },
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange,
        }
    });
}

function onPlayerReady(event) {
    function play(){
        $ytWrap.addClass('play');
        player.playVideo();
    }
    ytPlay.addEventListener('click', function() {
        play();
    });
    ytPreview.addEventListener('click', function() {
        play();
    });
    ytTitle.addEventListener('click', function() {
        play();
    });
}   

function onPlayerStateChange(event) {

    if(event.data == YT.PlayerState.PLAYING){
        $ytWrap.addClass('play');
    }
    
    /*if (event.data == YT.PlayerState.PAUSED) {
        $ytWrap.removeClass('play');
    }
    else if (event.data == YT.PlayerState.PLAYING) {
        $ytWrap.addClass('play');   
        $('video, audio').each(function() {
            this.pause();  
        });
    }
    else {
        return false;  
    }*/

}