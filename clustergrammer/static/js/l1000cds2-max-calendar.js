function get_calendar(popup, blanket){
	$.get('http://amp.pharm.mssm.edu/L1000CDS2/countByDate', function(data) {
		calendar = data;
		// calendar = [[2013,2,26,3],[2013,2,27,5]];
		draw_calendar(calendar, popup, blanket);
	});
}

function draw_calendar(calendar, popup, blanket){
	if (($(window).height()<=600)||($(window).width()<=1000)){mc = 0.75;}
	else{mc = 1;}
	
	var width = 960*mc,
    height = 136*mc,
    cellSize = 17*mc; // cell size

	var format = d3.time.format("%Y-%m-%d");
	
	// month
	var no_months_in_a_row = 12;
	var shift_up = cellSize * 7.3;
	
	var day = d3.time.format("%w"), // day of the week
	    day_of_month = d3.time.format("%e"), // day of the month
	    day_of_year = d3.time.format("%j"),
	    week = d3.time.format("%U"), // week number of the year
	    month = d3.time.format("%m"), // month number
	    year = d3.time.format("%Y"),
	    percent = d3.format(".1%"),
	    format = d3.time.format("%Y-%m-%d");
	// month
	
	var color = function(d){
	  if (d>=0 && d<100){return "#AAEEAA"}
	  else if (d>=100 && d<200){return "#95DD95"}
	  else if (d>=200 && d<300){return "#80CC80"}
	  else if (d>=300 && d<400){return "#6BBB6B"}
	  else if (d>=400 && d<500){return "#54A854"}
	  else if (d>=500 && d<600){return "#3F973F"}
	  else if (d>=600 && d<1000){return "#2A862A"}
	  else if (d>=1000 && d<5000){return "#157515"}
	  else if (d>=5000){return "#006400"};}
	
	var svg = d3.select("div#calendar-popup").selectAll("svg")
	    .data(d3.range(2015, 2016))
	  .enter().append("svg")
	    .attr("width", width)
	    .attr("height", height)
	  .append("g")
	    .attr("transform", "translate(" + ((width - cellSize * 53) / 2) + "," + (height - cellSize * 7 - 1) + ")");
	
	svg.append("text")
	    .attr("transform", "translate(-6," + cellSize * 3.5 + ")rotate(-90)")
	    .style("text-anchor", "middle")
	    .text(function(d) { return d; });
	
	var rect = svg.selectAll(".day")
	    .data(function(d) { return d3.time.days(new Date(d, 0, 1), new Date(d + 1, 0, 1)); })
	    .enter()
	    .append("rect")
	    .style("fill", "#BFFFBF")
	    .attr("class", "day")
	    .attr("width", cellSize*0.9)
	    .attr("height", cellSize*0.9)
	    .attr("x", function(d) {
	     window.today = new Date();
	     window.today_day = today.getDate();
	     window.today_month = today.getMonth()+1;
	     window.today_year = today.getYear()+1900;
	      return d3.time.weekOfYear(d) * cellSize; 
	    })
	    .attr("y", function(d) {return d.getDay() * cellSize;})
	    .style("stroke", function(d){
	          curr_day = d.getDate();
	          curr_month = d.getMonth()+1;
	          curr_year = d.getYear()+1900;
	      if ((curr_day === today_day)&&(curr_month === today_month)&&(curr_year === today_year)){
	        return "#f00";
	      }
	    })
	    .datum(format);
	
	// month
	var month_titles = svg.selectAll(".month-title")  // Jan, Feb, Mar and the whatnot
		.data(function(d) {
			return d3.time.months(new Date(d, 0, 1), new Date(d + 1, 0, 1)); })
		.enter().append("text")
	    .text(monthTitle)
	    .attr("x", function(d, i) {
	    	var month_padding = cellSize*4.5*((month(d)-1)%(no_months_in_a_row));
	    	return month_padding;})
	    .attr("y", function(d, i) {
	    	var week_diff = week(d) - week(new Date(year(d), month(d)-1, 1) );
	    	var row_level = Math.ceil(month(d) / (no_months_in_a_row));
	    	return (week_diff*cellSize) + row_level*cellSize*8 - cellSize - shift_up;})
	    .attr("class", "month-title")
	    .attr("d", monthTitle);
	// month
	
	// title for hovering over
	rect.append("title")
	    .text(function(d) { return d; });
	
	svg.selectAll(".month")
		.data(function(d) { return d3.time.months(new Date(d, 0, 1), new Date(d + 1, 0, 1)); })
		.enter().append("path")
	    .attr("class", "month")
	    .attr("d", monthPath);
	
	d3.csv("", function(error, csv) {
		if (error) throw error;
	    var legend = [];
		var values = [];
		var c_data = [];
		for (i = 0; i < calendar.length; i++){
			year = calendar[i][0];
			if(String(calendar[i][1]).length < 2){
				month = "0" + calendar[i][1];
			}
			else{
				month = calendar[i][1];
			};
			
			if(String(calendar[i][2]).length < 2){
				day = "0" + calendar[i][2];
			}
			else{
				day = calendar[i][2]; 
			};
			
			legend[i] = year+"-"+month+"-"+day;
			values[i] = calendar[i][3];
		}
		for (i = 0; i < calendar.length; i++){
			c_data[i] = {'Date': legend[i] , 'Value': values[i]};
		}
	
	  var data = d3.nest()
		  .key(function(d) { return d.Date; })
		  .rollup(function(d) { return d[0].Value; })
		  .map(c_data);
	  // fill rectangles with right color   
	  rect.filter(function(d) { return d in data; })
		  .style("fill", function(d) { return color(data[d]); })
		  .select("title")
		  .text(function(d) { return d + ": " + data[d] + " lists"; });
	});
	
	function monthPath(t0) {
	  var t1 = new Date(t0.getFullYear(), t0.getMonth() + 1, 0),
	      d0 = t0.getDay(), w0 = d3.time.weekOfYear(t0),
	      d1 = t1.getDay(), w1 = d3.time.weekOfYear(t1);
	  return "M" + (w0 + 1) * cellSize + "," + d0 * cellSize
	      + "H" + w0 * cellSize + "V" + 7 * cellSize
	      + "H" + w1 * cellSize + "V" + (d1 + 1) * cellSize
	      + "H" + (w1 + 1) * cellSize + "V" + 0
	      + "H" + (w0 + 1) * cellSize + "Z";
	};
	
	// month
	function monthTitle (t0) {
		var monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
		return monthNames[t0.getMonth()];
	};
	// month
	d3.select(self.frameElement).style("height", "2910px");
	centerPopup(popup, mc);
	loadPopup(popup, blanket);
}
	// d3
	
// pop-up
function showPopup() {
	var popup = $('div#calendar-popup');
	var blanket = $('div#blanket');
	get_calendar(popup, blanket);
}

function loadPopup(popup, blanket) {
	blanket.css({
		"opacity" : "0.65"
	});
	blanket.fadeIn();
	popup.fadeIn();
}

function disableAllPopup() {
	$('#blanket').fadeOut();
	$('.popup').fadeOut();
}

function centerPopup(popup, mc) {
	//request data for centering
	var popupHeight = popup.height();
	var popupWidth = popup.width();
	//centering
	popup.css({		
		'margin-top': -1*popupHeight*1.1,
		'margin-left': -1*popupWidth/2-10,
		'width': 960*mc,
	});
}
// pop-up