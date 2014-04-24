
function incrementSlider() {
    var currSliderVal = $('input#slider-0').slider("option", "value");
    if (currSliderVal == null)
    {
        currSliderVal = 1;
    }
    currSliderVal += 1;
    $('input#slider-0').slider("option", "value", currSliderVal);
    $('input[type="number"]#slider-0').val(currSliderVal).slider("refresh");
}

function updatePlayButton(isplaying) {
    playbutton = $('button#playbutton.ctrls');
    if (isplaying === "true")
    {
        if (window.sliderTimer)
        {
            clearInterval(window.sliderTimer);
        }
        window.sliderTimer = setInterval(incrementSlider, 1000);
        playbutton.text("Stop");
        playbutton.removeClass('ui-icon-arrow-r').addClass('ui-icon-delete');
        nowplaying = true
    }
    else
    {
        clearInterval(window.sliderTimer);
        playbutton.text("Play");
        playbutton.removeClass('ui-icon-delete').addClass('ui-icon-arrow-r');
        nowplaying = false
    }
}

$('.play').bind('click', function(event, ui) {
    console.log('was clicked for song ' + this.id.substring(5) );
    console.log(document.location.toString().toLowerCase());
    currentPageUrl = document.location.toString().toLowerCase();
    // empty post data means just start the song from the beginning
    var postdata = { };  // post the form values via ajax
    $.post(currentPageUrl, postdata, function(data) {
        if (data.playing)
        {
            updatePlayButton(data.playing);
        }
        if (data.artist && data.song)
        {
            $('h1#currentsong').text(data.artist + ' - ' + data.song);
        }
        if (data.duration)
        {
            // TODO
            console.log('setting max val to ' + data.duration);
            //$('input#slider-0').slider('option', 'max', data.duration);
            $('input#slider-0').attr('max', data.duration);
            //$('input[type="number"]#slider-0').slider('option', 'max', data.duration);
            $('input[type="number"]#slider-0').attr('max', data.duration);
        }
        $('input[type="number"]#slider-0').val(0).slider('refresh');
    });
    return true;
});

$('button#playbutton.ctrls').bind('click', function(event, ui) {
    if (nowplaying)
    {
        var postdata = 'playnow=false';  // post the form values via ajax
    }
    else
    {
        var postdata = 'playnow=true';  // post the form values via ajax
    }
    currentPageUrl = document.location.toString().toLowerCase();
    $.post(currentPageUrl, postdata, function(data) {
        if (data.playing && data.position)
        {
            console.log('data.position: ' + data.position);
            updatePlayButton(data.playing);
        }
    });
    return true;
});

