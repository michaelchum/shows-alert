$(document).ready(function() {

	// JQuery Code

	$('.rango-add').click(function(){
		var showid;
		showid = $(this).attr("data-showid");
		$.get('/rango/add_show/', {show_id: showid}, function(data){
			$('#list').html(data);
			//$('#add').hide();
		});
	});

});

// <button id ="add" data-showid="{{ show.id }}" class="btn btn-primary btn-small"><i class="icon-white icon-thumbs-up"></i> Follow</button>