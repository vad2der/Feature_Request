$client_drop_down = $('#client_drop_down');
$possible_priorities = $('#possible_priorities');
$production_area_drop_down = $('#production_area_drop_down');
$ticket_list = $('#ticket_list');

var ticketTemplate = "<li>"+
                        "<p>ID: {{id}}</p>"+
	                    "<p>Title: {{title}}</p>"+
	                    "<p>Client: {{client}}</p>"+
	                    "<p>Priority: {{client_priority}}</p>"+
	                    "<p>Target Date: {{target_date}}</p>"+
	                    "<p>Product Area: {{product_area}}</p>"+
	                    "<button id='edit' data-id='{{id}}'>Edit</Button><button id='delete' data-id='{{id}}'>Delete</Button>"
	                 "</li>";

// function to fill drop down menu with possible client names
var get_client_list = function() {
     $.ajax({
        type: 'GET',
	    url: '/api/client_list',
	    success: function(clients) {
	        $client_drop_down.find('option').remove();
	        $client_drop_down.append('<option disabled selected>..select a client..</option>');
	        $.each(eval(clients), function (i, client){
	            $client_drop_down.append('<option value="' + client + '">' + client + '</option>')
	        });
	    }
	 })
}
// listener to fill client names into drop down menu
$(window).load(get_client_list);


// function to show and fill priority drop down
var get_possible_priorities = function() {
     $.ajax({
        type: 'GET',
	    url: '/api/possible_priorities',
	    success: function(priorities) {
	        $possible_priorities.find('option').remove();
	        $.each(eval(priorities), function (i, priority){
	            $possible_priorities.append('<option value="' + priority + '">' + priority + '</option>')
	        });
	    }
	 })
}
// listener to fill priority drop down
$(window).load(get_possible_priorities);

// date picker
$('#date').datepicker({ dateFormat: 'D, d M yy', minDate: 0, maxDate: '+1y', showAnim: 'show'});


// production area drop down
var get_production_areas = function() {
     $.ajax({
        type: 'GET',
	    url: '/api/production_areas',
	    success: function(areas) {
	        $production_area_drop_down.find('option').remove();
	        $production_area_drop_down.append('<option disabled selected>..select an area..</option>');
	        $.each(eval(areas), function (i, area){
	            $production_area_drop_down.append('<option value="' + area + '">' + area + '</option>')
	        });
	    }
	 })
}
// listener to fill prod area drop down menu
$(window).load(get_production_areas);

// helper to show buttons
var show_proper_buttons = function(){
    if ($('#ticket_id').val().length > 0){
        $('#submit').hide();
        $('#update').show();
    } else{
        $('#submit').show();
        $('#update').hide();
    }
}
// listener to trigger show_proper_buttons
$('#id').change(show_proper_buttons);

var check_fields = function (object){
    var check = true;
    if ($('#ticket_title').val().length == 0){
        check = false;
        $('#ticket_title').toggle("bounce", {times: 2});
        $('#ticket_title').show(50);
    }
    if ($('#ticket_description').val().length == 0){
        check = false
        $('#ticket_description').toggle("bounce", {times: 2});
        $('#ticket_description').show(50);
    }
    if($('#client_drop_down').val() == null || $('#client_drop_down').val() == '..select a client..'){
        $('#client_drop_down').toggle("bounce", {times: 2});
        $('#client_drop_down').show(50);
    }
    if ($('#date').val().length == 0){
        $('#date').toggle("bounce", {times: 2});
        $('#date').show(50);
    }
    if($('#production_area_drop_down').val() == null || $('#production_area_drop_down').val() == '..select an area..'){
        $('#production_area_drop_down').toggle("bounce", {times: 2});
        $('#production_area_drop_down').show(50);
    }
}

//function to insert a new ticket
var insert_new_ticket = function(){
    var d = $('#date').val();
    var a = JSON.stringify(d).slice(1,4);
    var day = JSON.stringify(d).slice(6,8);
    var mm = JSON.stringify(d).slice(9,12);
    var yy = JSON.stringify(d).slice(13, 17);
    //alert('wd: '+a+', d: '+day+', m: '+mm+', y: '+yy)
    var date = a+', '+day+' '+mm+' '+yy;
    var new_request={
        title: $('#ticket_title').val(),
        description: $('#ticket_description').val(),
        client: $('#client_drop_down').val(),
        client_priority: $('#possible_priorities').val(),
        target_date: date,
        product_area: $('#production_area_drop_down').val(),
        url_root: window.location.hostname
    };
    if(check_fields(new_request)){
        $.ajax({
			type: 'POST',
			url: '/api/ticket/new',
			data: new_request,
			success: function() {
				$('#ticket_title').empty();
				$('#ticket_description').empty();
				$('#date').empty();
				get_client_list();
				get_possible_priorities();
				get_production_areas();
				get_existing_tickets();
			},
			error: function() {
				alert('Error inserting new request');
			}
		});
	} else {
	    alert('All fields should be filled');
	}
}
$('#submit').click(insert_new_ticket);

// fuction to  transfert data from li to form
var transferDataToEdit = function(li){
    //TODO: populate data
    //alert(li);
    $('#ticket_id').closest('tr').show(50);
    //$('#ticket_id').val(li.find('#id').html())
    //$('#ticket_title').val(li.find('#title').html());
    $('#ticket_url').closest('tr').show(50);
}

$('#ticket_list').delegate('#edit', 'click', function(){
    $li = $(this).closest('li');
     transferDataToEdit($li);
});

// function to list existing entries
var get_existing_tickets = function(){
     $.ajax({
        type: 'GET',
	    url: '/api/ticket/all',
	    success: function(tickets) {
	        $ticket_list.empty();
	        $.each(tickets, function (i, ticket){
	            ticket.target_date = ticket.target_date.slice(0,17)
	            $ticket_list.append(Mustache.render(ticketTemplate, ticket))
	        });
	    }
	 })
}
$(window).load(get_existing_tickets);
// function to edit an existing entry


//function to remove an existing entry