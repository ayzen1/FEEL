var chart; // globally available
var test;
function newChart()
{
	chart = new Highcharts.StockChart({
        chart: {
           renderTo: 'eda-graph-div',
           defaultSeriesType: 'spline',
           events: {
               //load: requestData
            }
        },
        title: {
            text: 'Live random data'
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 150,
            maxZoom: 20 * 1000
        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'Value',
                margin: 80
            }
        },
        
        series: [{
            name: 'Random data',
            pointStart: Date.UTC(2004, 3, 1), // first of April
            pointInterval: 3600 * 1000, // hourly
            data: test
        }], 
     });	
};