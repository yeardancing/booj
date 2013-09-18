function updateControls() 
{
    $('#slider-0').val(50);
    $('#slider-0').slider('refresh');
    if ($('#playbutton').prev('span').find('span.ui-btn-text').text() == "Play")
    {
        $('#playbutton').prev('span').buttonMarkup({ icon: "delete" });
        $('#playbutton').prev('span').find('span.ui-btn-text').text("Stop");
    }
    else
    {
        $('#playbutton').prev('span').buttonMarkup({ icon: "arrow-r" });
        $('#playbutton').prev('span').find('span.ui-btn-text').text("Play");
    }
};
