function updateControls() 
{
    $('#slider-0').val(90);
    $('#slider-0').slider('refresh');
    $('#playbutton').button('refresh');
    console.log('isPlaying');
    /*
    if ()
    {
        $('#playbutton').prev('span').buttonMarkup({ icon: "delete" });
        $('#playbutton').prev('span').find('span.ui-btn-text').text("Stop");
    }
    else
    {
        $('#playbutton').prev('span').buttonMarkup({ icon: "arrow-r" });
        $('#playbutton').prev('span').find('span.ui-btn-text').text("Play");
    }
    */
};
