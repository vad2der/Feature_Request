$client_drop_down = $('#client_drop_down');
$possible_priorities = $('#possible_priorities');
$production_area_drop_down = $('#production_area_drop_down');
$ticket_list = $('#ticket_list');

var ticketTemplate = "<li>"+
                        "<p class='id' data='{{id}}'>ID: {{id}}</p>"+
	                    "<p class='title' data='{{title}}'>Title: {{title}}</p>"+"<p class='description' data='{{description}}' hidden>Description: {{description}}</p>"+
	                    "<p class='client' data='{{client}}'>Client: {{client}}</p>"+
	                    "<p class='client_priority' data='{{client_priority}}'>Priority: {{client_priority}}</p>"+
	                    "<p class='target_date' data='{{target_date}}'>Target Date: {{target_date}}</p>"+"<p class='ticket_url' data='{{ticket_url}}' hidden>URL: {{ticket_url}}</p>"+
	                    "<p class='product_area' data='{{product_area}}'>Product Area: {{product_area}}</p>"+
	                    "<button id='edit' data-id='{{id}}'>Edit</button>"+
						"<button id='delete' data-id='{{id}}'>Delete</button>"+
						"<button id='open' data-id='{{id}}'>Open</button>"+
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
			priorities = eval(priorities).sort().reverse();
	        $possible_priorities.find('option').remove();
	        $.each(priorities, function (i, priority){
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
    if ($('#ticket_id').text().length > 0){
        $('#submit').closest('button').hide();
        $('#update').closest('button').show();
    } else{
        $('#submit').closest('button').show();
        $('#update').closest('button').hide();
    }
}

var check_fields = function (object){
    var check = true;
    if ($('#ticket_title').val().length == 0 || $('#ticket_title').val() == 'Input title of your request'){
        check = false;
        $('#ticket_title').toggle("bounce", {times: 2});
        $('#ticket_title').show(50);
    }
    if ($('#ticket_description').val().length == 0 || $('#ticket_description').val() == 'Input concise description of your request'){
        check = false;
        $('#ticket_description').toggle("bounce", {times: 2});
        $('#ticket_description').show(50);
    }
    if($('#client_drop_down').val() == null || $('#client_drop_down').val() == '..select a client..'){
        check = false;
		$('#client_drop_down').toggle("bounce", {times: 2});
        $('#client_drop_down').show(50);
    }
    if ($('#date').val().length == 0){
        check = false;
		$('#date').toggle("bounce", {times: 2});
        $('#date').show(50);
    }
    if($('#production_area_drop_down').val() == null || $('#production_area_drop_down').val() == '..select an area..'){
        check = false;
		$('#production_area_drop_down').toggle("bounce", {times: 2});
        $('#production_area_drop_down').show(50);
    }
	return check;
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
        url_root: window.location.origin
    };
    if(check_fields(new_request)){
        $.ajax({
			type: 'POST',
			url: '/api/ticket/new',
			data: new_request,
			success: function() {
				$('#ticket_title').val('Input title of your request');
				$('#ticket_description').val('Input concise description of your request');
				$('#date').val('Pick a date');
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
    $('#ticket_id').text(li.find('.id').attr('data'))
    $('#ticket_title').val(li.find('.title').attr('data'));
    $('#ticket_url').closest('tr').show(50);
	$('#ticket_description').val(li.find('.description').attr('data'));
	$('#client_drop_down').val(li.find('.client').attr('data'));
	$('#possible_priorities').val(li.find('.client_priority').attr('data'));
	$('#date').val(li.find('.target_date').attr('data'));
	$('#ticket_url').text(li.find('.ticket_url').attr('data'));
	$('#production_area_drop_down').val(li.find('.product_area').attr('data'));
}

$('#ticket_list').delegate('#edit', 'click', function(){
    $li = $(this).closest('li');
     transferDataToEdit($li);
	 show_proper_buttons();
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
	    },
		error: function() {
		    alert('Error getting existing requests');
	    }
	 })
}
$(window).load(get_existing_tickets);

// reset button
var reset = function(){
	$('#ticket_title').val('Input title of you request');
				$('#ticket_id').text('');
				$('#ticket_id').closest('tr').hide(50);
				$('#ticket_url').text('');
				$('#ticket_url').closest('tr').hide(50);
				$('#ticket_description').val('Input concise description of your request');
				$('#date').val('Pick a date');
				get_client_list();
				get_possible_priorities();
				get_production_areas();
				get_existing_tickets();
				show_proper_buttons();
}
$('#reset').click(reset);

// function to edit an existing entry
var update_entry = function(){
	var d = $('#date').val();
    var a = JSON.stringify(d).slice(1,4);
    var day = JSON.stringify(d).slice(6,8);
    var mm = JSON.stringify(d).slice(9,12);
    var yy = JSON.stringify(d).slice(13, 17);
    //alert('wd: '+a+', d: '+day+', m: '+mm+', y: '+yy)
    var date = a+', '+day+' '+mm+' '+yy;
	var request={
		id: $('#ticket_id').text(),
        title: $('#ticket_title').val(),
        description: $('#ticket_description').val(),
        client: $('#client_drop_down').val(),
        client_priority: $('#possible_priorities').val(),
        target_date: date,
        product_area: $('#production_area_drop_down').val(),
        url_root: window.location.origin.toString()
		};
	//alert(JSON.stringify(request));
	$.ajax({
		type: 'PUT',
		url: '/api/ticket/update',
		data: request,
		success:function() {
			reset();
		    get_existing_tickets();				
	    },
		error: function() {
		    alert('Error updating collection');
	    }
	});
}
$('#update').click(update_entry);

//function to remove an existing entry
var delete_entry = function (li) {	
	var ticket = {id: li.find('.id').attr('data')}
	$.ajax({
		    type: 'DELETE',
			data: ticket,
		    url: '/api/ticket/delete',
		    success: function() {
				get_existing_tickets();
		    },
		    error: function() {
			    alert('error deleting the entry');
		    }
	    });
}
$('#ticket_list').delegate('#delete', 'click', function(){
    $li = $(this).closest('li');
     delete_entry($li);
});

//click on an item in the list
$('#ticket_list').delegate('#open', 'click', function(){
    $li = $(this).closest('li');
    var id = $li.find('.id').attr('data');
	var url = window.location.origin.toString() + '/ticket/' + id.toString();
	window.open(url);
  return false;
});
