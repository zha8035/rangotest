$(document).ready(function()
{
    //alert("Hello, world!");
    $('#about-btn').click(function(){
        alert('you clicked the button using jquery')
    })
    // $('p').hover()(
    //     function(){
    //         $('p').css('color','red');
    //     },
    //     function(){
    //         $('p').css('color','black');
    //     }
    // );

    $('p').hover(
        function() {
            $(this).css('color', 'red');
        },
        function() {
            $(this).css('color', 'black');
        }
    );
});