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

/* to toggle panels in admin */
function minimize_panel(panel_body_id, panel_btn) {
    var panel = document.getElementById(panel_body_id);
    $(panel).slideToggle();
    var btn = document.getElementById(panel_btn);
    $(btn).toggleClass("glyphicon glyphicon-chevron-down glyphicon glyphicon-chevron-up");  
}
