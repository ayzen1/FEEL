$(document).ready(function(){ 
  $("#events").jqGrid({
    url:'/populate',
    datatype: 'json',
    mtype: 'GET',
    colNames:['Type','Time', 'Memo', 'Event_ID',],
    colModel :[ 
      {name:'event_type', index:'event_type', resizable:'false', width:55}, 
      {name:'event_time', index:'event_time', width:90, align:'right'}, 
      {name:'event_memo', index:'event_memo', width:80, align:'right', sortable:'false'},
      {name:'event_id', hidden:'true', sortable:'false'},
    ],
    jsonReader: {
    	root: "events",    	
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