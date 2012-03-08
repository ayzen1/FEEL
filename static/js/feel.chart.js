var chart;

function newChart(start_time, incoming_data){
	var startTime = Date.parse(start_time);
	chart = new Highcharts.StockChart({
	    chart: {
	       renderTo: 'eda-graph-div',
	       defaultSeriesType: 'spline'
	    },
	    title: {
	        text: 'EDA Graph',
	    },
	    xAxis: {
	        type: 'datetime',
	        //minRange: 5*60*100, // 5 min
	        tickPixelInterval: 150,
	        maxZoom: 20 * 1000
	    },
	    legend:{
	    	enabled:true,
	    	align:'center',
	    	x:150,
	    	y: 20,
	    	verticalAlign:'top',
	    	layout:'vertical',
	    	borderColor: 'black',
            borderWidth: 2,
	    },
	    yAxis: [{
					id: 'eda-y-axis',
					minPadding: 0.2,
					maxPadding: 0.2,
					title: {
						text: 'EDA',
						margin: 10
						}
	    		},{
					id: 'temp-y-axis',
					minPadding: 0.2,
					maxPadding: 0.2,
					title: {
						text: 'Temperature',
						margin: 10
						}
				},{
					id: 'accx-y-axis',
					minPadding: 0.2,
					maxPadding: 0.2,
					opposite:true,
					title: {
						text: 'Acc X',
						margin: 10
						}
				},{
					id: 'accy-y-axis',
					minPadding: 0.2,
					maxPadding: 0.2,
					opposite:true,
					title: {
						text: 'Acc Y',
						margin: 10
						}
				},{
					id: 'accz-y-axis',
					minPadding: 0.2,
					maxPadding: 0.2,
					opposite:true,
					title: {
						text: 'Acc Z',
						margin: 10
						}
			}],
	    
	    series: 
	        [{
	        	name: 'EDA',
	            data: incoming_data.eda,
	            pointStart: startTime,
	            pointInterval: 125,
	        } ,{
	        	name: 'Temperature',
	        	data: incoming_data.temp,
	        	pointStart: startTime,
	        	pointInterval: 125,
	        },{
	        	name: 'Acc-X',
	        	data: incoming_data.acc_x,
	        	pointStart: startTime,
	        	pointInterval: 125,
	        },{
	        	name: 'Acc-Y',
	        	data: incoming_data.acc_y,
	        	pointStart: startTime,
	        	pointInterval: 125,
	        },{
	        	name: 'Acc-Z',
	        	data: incoming_data.acc_z,
	        	pointStart: startTime,
	        	pointInterval: 125,
	        }]
	
	    
	 });
}