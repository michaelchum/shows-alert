$(document).ready(function() {


        $('.rango-add').click(function(){
                var showid;
                showid = $(this).attr("data-showid");
                 $.get('/rango/add_show/', {show_id: showid}, function(data){
                           $('#list').html(data);
                           initBinding();
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

}