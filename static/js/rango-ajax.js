$(document).ready(function() {

	initBinding();

});

function initBinding() 
{
		$('.rango-add').click(function(){
                var showid;
                showid = $(this).attr("data-showid");
                 $.get('/rango/add_show/', {show_id: showid}, function(data){
                           $('#list').html(data);
                           initBinding() 
                       });
            });

        $('.remove_show').click(function(){
                var showid;
                showid = $(this).attr("data-showid");
                 $.get('/rango/remove_show/', {show_id: showid}, function(data){
                           $('#list').html(data);
                           initBinding() 
                       });
            });

        /*

        $('.rango-add').hover(function () {
            $(this).removeClass('btn-primary');
            $(this).addClass('btn-inverse');
        }, function () {
            $(this).removeClass('btn-inverse');
            $(this).addClass('btn-primary');
            initBinding() 
        });

		*/

		$('.rango-remove').click(function(){
                var showid;
                showid = $(this).attr("data-showid");
                 $.get('/rango/remove_show2/', {show_id: showid}, function(data){
                           $('#list').html(data);
                           initBinding() 
                       });
            });

        $('#suggestion').keyup(function(){
                var query;
                query = $(this).val();
                $.get('/rango/suggest_category/', {suggestion: query}, function(data){
                	$('#cats').html(data);
                	initBinding() 
                });
        });
      $('.add_email').click(function(){
           $.get('/rango/add_email/', {show_id: 5}, function(data){
                     $('#list').html(data);
                     initBinding() 
                 });
      });
      $('.remove_email').click(function(){
           $.get('/rango/remove_email/', {show_id: 5}, function(data){
                     $('#list').html(data);
                     initBinding() 
                 });
      });
            $('.add_sms').click(function(){
           $.get('/rango/add_sms/', {show_id: 5}, function(data){
                     $('#list').html(data);
                     initBinding() 
                 });
      });
      $('.remove_sms').click(function(){
           $.get('/rango/remove_sms/', {show_id: 5}, function(data){
                     $('#list').html(data);
                     initBinding() 
                 });
      });
    /*
    $('.remove_show').hover(function () {
        $(this).removeClass('btn-success');
        $(this).addClass('btn-warning');
        $('i', this).removeClass('icon-ok');
        $('i', this).addClass('icon-remove');
    }, function () {
        $(this).removeClass('btn-warning');
        $(this).addClass('btn-success');
        $('i', this).removeClass('icon-remove');
        $('i', this).addClass('icon-ok');
        initBinding();
    });
    */
            $('.remove_from_show').click(function(){
                var showid;
                showid = $(this).attr("data-showid");
                 $.get('/rango/remove_from_show/', {show_id: showid}, function(data){
                           $('#list').html(data);
                           initBinding() 
                       });
            });
            $('.add_from_show').click(function(){
                var showid;
                showid = $(this).attr("data-showid");
                 $.get('/rango/add_from_show/', {show_id: showid}, function(data){
                           $('#list').html(data);
                           initBinding() 
                       });
            });
}

