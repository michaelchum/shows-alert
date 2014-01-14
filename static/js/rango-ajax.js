$(document).ready(function() {

	// JQuery Code

	$('#add').click(function(){
		var showid;
		showid = $(this).attr("data-showid");
		$.get('/rango/add_show/', {show_id: showid}, function(data){
			$('#added_count').html(data);
			$('#add').hide();
		});
	});

	$('#suggestion').keyup(function(){
        var query;
        query = $(this).val();
        $.get('/rango/suggest_category/', {suggestion: query}, function(data){
         $('#cats').html(data);
        });
});

});