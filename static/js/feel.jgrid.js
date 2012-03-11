var selectedRow = null; // global variable
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
		  {name:'event_time', index:'event_time', align:'center', width:230, fixed:'true', formatter:timeFormatter}, 
		  {name:'event_memo', index:'event_memo', align:'left', width:400, sortable:'false'},
		  {name:'event_id', hidden:'true', sortable:'false'},
		],
		jsonReader: {
			root: "events",    	
		},
		onSelectRow: function(id){
			selectedRow = $("#events-grid").getRowData(id);
			
			var event_type = $("#events-grid").getRowData(id).event_type;
			var event_time = $("#events-grid").getRowData(id).event_time;
			var event_id = $("#events-grid").getRowData(id).event_id;
			
			// make ajax request to server if popup should be displayed			
			$.ajax({url:'/feedback', 
					type:'GET',
					dataType: 'json', 
					data:{'type':'should_popup','event_type':event_type, 'event_id':event_id},
					success: function(data, textStatus, jqXHR){
							// if response is positive use popup window to get feedback
							if(data.response == "yes"){
								centerPopupDiv('#feedback-div');
								loadPopupDiv('#feedback-div');
								// request event details
						
								$.ajax({
									url:'/event_get', 
									type:'GET',
									dataType: 'json', 
									data:{'event_type':event_type, 'event_id':event_id},
									success: function(data, textStatus, jqXHR){
										 // loadEventIntoFeedback(data);
										} 
									});
							}
					} 
				});
			
			$.ajax({
				url:'/eda_get', 
				type:'GET',
				dataType: 'json', 
				data:{'event_type':event_type, 'event_id':event_id},
				success: function(data, textStatus, jqXHR){
					newChart(event_time, data);
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
	  }); 

});
function timeFormatter(cellvalue, options, rowObject){
	var ms = Date.parse(cellvalue);
	var d = new Date(0);
	d.setUTCSeconds(ms/1000);
	return d.toLocaleDateString() +" "+ d.toLocaleTimeString();
	
}