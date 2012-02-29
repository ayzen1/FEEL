$(document).ready(
	function(){ 
	  $("#events-grid").jqGrid({
		url:'/populate',
		datatype: 'json',
		mtype: 'GET',
		altclass:'true',
		colNames:['Type','Time', 'Memo', 'Event ID',],
		colModel :[ 
		  {name:'event_type', index:'event_type', align:'center', width:80, fixed:'true'}, 
		  {name:'event_time', index:'event_time', align:'center', width:150, fixed:'true'}, 
		  {name:'event_memo', index:'event_memo', align:'left', width:500, sortable:'false'},
		  {name:'event_id', hidden:'true', sortable:'false'},
		],
		jsonReader: {
			root: "events",    	
		},
		onSelectRow: function(id){
			var event_type = $("#events-grid").getRowData(id).event_type;
			var event_id = $("#events-grid").getRowData(id).event_id;
			$.ajax({
				url:'/eda_get', 
				type:'GET',
				dataType: 'json', 
				data:{'event_type':event_type, 'event_id':event_id},
				success: function(data, textStatus, jqXHR){
					test = data.eda;
					newChart();
				} 
				});
		},
		pager: '#pager',
		rowNum:10,
		rowList:[10,20,30],
		sortname: 'event_time',
		sortorder: 'desc',
		viewrecords: true,
		gridview: true,
		caption: 'My first grid'
	  }); 

});