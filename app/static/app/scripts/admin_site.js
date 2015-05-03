function plot_confidence(data) {
    flot_data = []
    Object.keys(data).forEach(function (key) {
    	var value = data[key]
    	color = ''
    	/* place in each if statement to prevent key 'current' from being in the graph */
    	if (key=='good') {
    		color="#5cb85c"
    		flot_data.push({label: key, data: value, color: color})
    	}
    	if (key=='neutral') {
    		color="#f0ad4e"
    		flot_data.push({label: key, data: value, color: color})
    	}
    	if (key=='bad') {
    		color="#d9534f"
    		flot_data.push({label: key, data: value, color: color})
    	}
    });
	$.plot('#confidence-graph', flot_data, {
    series: {
        pie: {
            show: true
        	}
    	}
    });
}

var ping_interval = 1000*15
setInterval(function() {
    $.ajax({
        type: "GET",
        url:  "/poll/",
        dataType: 'json',
        success: function (data) {
        	plot_confidence(data)
        },
        error: function(response){
        },
	});
    }, ping_interval
)

function quick_update(data_id, value, csrf_token) {
	data = {
		'csrfmiddlewaretoken': csrf_token,
		'quick_settings': 'Submit',
	}
	data[data_id] = value
	$.ajax({
		type: "POST",
		url:  "/quick_update/",
		dataType: 'json',
		data: data,
		success: function (data) {
			if (data.return_type == 'lecture') {
				$('#id_Lecture').attr("value", data.return_value);	
			}
			if (data.return_type == 'quiz') {
				$("#quick_quiz_select option[value='" + data.return_value + "']").remove();
				$("#quiz-result-summary").load(" #quiz-result-summary", function() {$(this).children().unwrap()});
			}
			if (typeof data.notice !== 'undefined') {
				close_button = 	'<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
								'<span aria-hidden="true">&times;</span>' +
								'</button>'
				$("#admin_alerts").html('<div class="alert alert-success alert-dismissable" role="alert">' + data.notice + close_button + '</div>')
			}
		},
		error: function(response){
		},
	});
}

function addQuickSelectHandlers() {
	$("#quick_lecture_select").change(function(data) {
		quick_update('lecture', this.options[this.selectedIndex].value, "{{csrf_token}}")
	});
	$("#quick_quiz_select").change(function(data) {
		quick_update('quiz', this.options[this.selectedIndex].value, "{{csrf_token}}")
	});
}

/* to toggle panels in admin */
function minimize_panel(panel_body_id, panel_btn) {
    var panel = document.getElementById(panel_body_id);
    $(panel).slideToggle();
    var btn = document.getElementById(panel_btn);
    $(btn).toggleClass("glyphicon glyphicon-chevron-down glyphicon glyphicon-chevron-up");  
}

