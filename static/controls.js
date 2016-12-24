function boojPageInit() {
	if (typeof songInfo === "undefined") {
		songInfo = {
			title			: "none",
            isplaying 		: "false",
			duration 		: null,
            sliderValue     : 1
		};
	}

    $('h1#currentsong').text(songInfo.title);
	updatePlayButton(songInfo.isplaying);
}

function incrementSlider() {
    var currSliderVal = $('input#slider-0').slider("option", "value");
    currSliderVal += 1;
    $('input#slider-0').slider("option", "value", currSliderVal);
    $('input[type="number"]#slider-0').val(currSliderVal).slider("refresh");
}

function updatePlayButton(isplaying) {
    playbutton = $('button#playbutton.ctrls');
    if (isplaying === "true")
    {
        //if (window.sliderTimer)
        //{
        //    clearInterval(window.sliderTimer);
        //}
        //window.sliderTimer = setInterval(incrementSlider, 1000);
        playbutton.text("Stop");
        playbutton.removeClass('ui-icon-arrow-r').addClass('ui-icon-delete');
        nowplaying = true
    }
    else
    {
        //clearInterval(window.sliderTimer);
        playbutton.text("Play");
        playbutton.removeClass('ui-icon-delete').addClass('ui-icon-arrow-r');
        nowplaying = false
    }
}

// play button logic (song page only)
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
            var title = data.artist + ' - ' + data.song;
            $('h1#currentsong').text(title);

        }
        if (data.duration)
        {
            // TODO
            var duration = data.duration;
            var sliderValue = 1;
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

// bottom panel controls logic 
$('button#playbutton.ctrls').bind('click', function(event, ui) {
    var button = $('button#playbutton.ctrls').text();
    console.log('button=' + button);
    if (button === "Stop" || button === "StopStop") {
        var postdata = 'playnow=false';  // post the form values via ajax
    }
    else {
        var postdata = 'playnow=true';  // post the form values via ajax
    }
    currentPageUrl = document.location.toString().toLowerCase();
    $.post(currentPageUrl, postdata, function(data) {
        if (data.playing && data.position)
        {
            console.log('data.position: ' + data.position);
            console.log('data.playing: ' + data.playing);
            updatePlayButton(data.playing);
        }
    });
    return true;
});


// get slider position from previous page
$(document).on('pagebeforeshow', function(e, data){     
    var button = data.prevPage.find('button#playbutton.ctrls').text();
    var isplaying = "false";
    if (button === "Stop") {
        isplaying = "true";
    }
    updatePlayButton(isplaying);

    var title = data.prevPage.find('h1#currentsong').text();
    $('h1#currentsong').text(title);
    /*
    if (sliderValue === undefined) {
        console.log('previous value was undefined')
    }
    else {
        console.log('prev page val is ' + sliderValue);
    }
    sliderValue = $('input#slider-0').slider("option", "value");
    console.log('this page val is ' + sliderValue);
    $('input#slider-0').slider("option", "value", sliderValue);
    $('input[type="number"]#slider-0').val(sliderValue).slider("refresh");
    */
});

