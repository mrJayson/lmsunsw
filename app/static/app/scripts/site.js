/* for toggling the menu during mobile view */

$("#menu-toggle").click(function(e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
    $("#toggle-arrow").toggleClass("glyphicon glyphicon-chevron-right white glyphicon glyphicon-chevron-left white");
});

function refresh_confidence(data) {
    $("#progress-bar-good").attr("style", "width: "+ data.good +"%");
    $("#progress-bar-neutral").attr("style", "width: "+ data.neutral +"%");
    $("#progress-bar-bad").attr("style", "width: "+ data.bad +"%");
    if (data.current == 1) {
        $("#good-btn").html("good<span class='glyphicon glyphicon-ok'></span>")
    } else {
        $("#good-btn").html("good")
    }
    if (data.current == 0) {
        $("#neutral-btn").html("neutral<span class='glyphicon glyphicon-ok'></span>")
    } else {
        $("#neutral-btn").html("neutral")
    }
    if (data.current == -1) {
        $("#bad-btn").html("bad<span class='glyphicon glyphicon-ok'></span>")
    } else {
        $("#bad-btn").html("bad")
    }
}

function student_poll(current_quiz_list) {
    /* send data in poll to compare and retrieve if needed */
    
    $.ajax({
        type: "GET",
        url:  "/student_poll/",
        dataType: 'json',
        data: {'quiz_length': current_quiz_list},
        success: function (data) {
            /* update confidence meter */
            refresh_confidence(data)
            /* update new quiz badge number */
            if (data.quiz_difference > 0) {
                $('#current_quiz_list').load(' #current_quiz_list', function() {$(this).children().unwrap()})
                $.notify("quiz closed")
            }
            else if (data.quiz_difference < 0) {
                $('#current_quiz_list').load(' #current_quiz_list', function() {$(this).children().unwrap()})
                $.notify("new quiz available")
            }
        },
        error: function(response){
        },
    });
}

function vote(vote) {
    vote = typeof vote !== 'undefined' ? {vote:vote} : {};
    $.ajax({
        type: "GET",
        url:  "/vote/",
        dataType: 'json',
        data: vote,
        success: function (data) {
            refresh_confidence(data)
        },
        error: function(response){

        },
    });
}

/* to trigger ajax request for confidence meter */
function addClickHandlers() {
    $("#good-btn").click( function() { vote(1) });
    $("#neutral-btn").click( function() { vote(0) });
    $("#bad-btn").click( function() { vote(-1) });
}
$(document).ready(addClickHandlers);


