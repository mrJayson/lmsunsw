function plot_confidence(data) {
    flot_data = []
    Object.keys(data).forEach(function (key) {
    	var value = data[key]
    	color = ''
    	/* place in each if statement to prevent key 'current' from being in the graph */
    	if (key=='good_confidence_meter_data') {
    		color="#5cb85c"
    		flot_data.push({label: 'good', data: value, color: color})
            $("#good_confidence_meter_data").html('Good: '+data[key])
    	}
    	if (key=='neutral_confidence_meter_data') {
    		color="#f0ad4e"
    		flot_data.push({label: 'neutral', data: value, color: color})
            $("#neutral_confidence_meter_data").html('Neutral: '+data[key])
    	}
    	if (key=='bad_confidence_meter_data') {
    		color="#d9534f"
    		flot_data.push({label: 'bad', data: value, color: color})
            $("#bad_confidence_meter_data").html('Bad: '+data[key])
    	}
        if (key=='bad_left') {        
            $("#bad-seat-location-left").html(data[key])
        }
        if (key=='bad_middle') {
            $("#bad-seat-location-middle").html(data[key])
        }
        if (key=='bad_right') {
            $("#bad-seat-location-right").html(data[key])
        }
    });
	$.plot('#confidence-graph', flot_data, {
        series: {
            pie: {
                show: true,
                radius: 1,
                label: {
                    show: true,
                    radius: 3/4,
                    background: {
                        opacity: 0.5,
                        color: '#000',
                    }
                },
        	}
    	}
    });
}

function update_confidence_messages(data) {
    
    html = "";
    for (var i = 0; i < data.length; i++) {
        if (data[i]['confidence_message'] != null || data[i]['user'] != null ) {
            html += "<tr><td>"+data[i]['user']+"</td><<td>"+data[i]['confidence_message']+"</td></tr>";
        }
    }
    $("#confidence-messages").html(html)
}

var ping_interval = 1000
setInterval(function() {
    $.ajax({
        type: "GET",
        url:  "/admin_poll/",
        dataType: 'json',
        success: function (data) {
        	plot_confidence({
                'good_confidence_meter_data':data['good_confidence_meter_data'], 
                'neutral_confidence_meter_data':data['neutral_confidence_meter_data'], 
                'bad_confidence_meter_data':data['bad_confidence_meter_data'],
                'bad_left':data['bad_left'],
                'bad_middle':data['bad_middle'],
                'bad_right':data['bad_right']
            });
            update_confidence_messages(data['confidence_messages']);
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
				$("#quick-settings-panel").load(" #quick-settings-panel", function() {$(this).children().unwrap()});
			}
            if (data.return_type == 'quiz_close') {
                $("#quick-settings-panel").load(" #quick-settings-panel", function() {$(this).children().unwrap()});
            }
            if (data.return_type == 'quiz_open') {
                $("#quick-settings-panel").load(" #quick-settings-panel", function() {$(this).children().unwrap()});
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

/* to toggle panels in admin */
function minimize_panel(panel_body_id, panel_btn) {
    var panel = document.getElementById(panel_body_id);
    $(panel).slideToggle();
    var btn = document.getElementById(panel_btn);
    $(btn).toggleClass("glyphicon glyphicon-chevron-down glyphicon glyphicon-chevron-up");  
}

