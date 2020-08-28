// Call the dataTables jQuery plugin
$(document).ready(function() {
  var table = $('#dataTable').DataTable({
  	serverSide: true,
	processing: true,
                ajax: {
                    url: '../table_ajax/flags',
                    dataSrc: 'data',
                    type: 'GET',
                    data: function (args) {
                        //args.qString = getQuerystring(); //add in querystring args, or anything else you want
                        return {
                            "args": JSON.stringify(args)
                        };
                    }
                },
                columns: [
                    {data: 'IP'},
                    {data: 'target'},
                    {data: 'exploit'},
                    {data: 'flag'},
                    {data: 'timestamp'},
                    {data: 'status'}
                ],
                order: [[ 4, "desc" ],[2,"asc"],[5,"asc"]]
  
  });
  
  setInterval( function () {
    table.ajax.reload(null,false);
}, 10000 );
});

