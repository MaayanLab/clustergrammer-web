function ini_play_button(){

  // playback instructions 
  demo_text_box = d3.select('#play_button')
    .attr('id','demo_text_box')
    .style('display','none');

  // get dimensions of the main_svg
  var dim = {};
  dim.main_svg = {};
  dim.main_svg.w = d3.select('#main_svg').style('width').replace('px','');
  dim.main_svg.h = d3.select('#main_svg').style('height').replace('px','');

  demo_text_box
    .append('rect') 
    .attr('width',200)
    .attr('height',100)
    // .attr('transform', function(){
    //     var pos_x = dim.main_svg.w/2;
    //     var pos_y = dim.main_svg.h/2;
    //     return 'translate('+pos_x+','+pos_y+')';
    //   })
    .style('opacity',0.5);


  // add preview button for demo 
  var play_button = d3.select('#main_svg')
    .append('g')
    .attr('id','play_button');

  play_button
    .attr('transform', function(){
      var pos_x = dim.main_svg.w/2;
      var pos_y = dim.main_svg.h/2;
      return 'translate('+pos_x+','+pos_y+')';
    });
    
  play_button
    .append('circle')
    .style('r',45)
    .style('fill','white')
    .style('stroke','black')
    .style('stroke-width','3px')
    .style('opacity',0.5);

  play_button
    .append('path')
    .attr('d',function(){

      var tri_w = 40;
      var tri_h = 22; 
      var tri_offset = 15;

      return 'M-'+tri_offset+',-'+tri_h+' l '+tri_w+','+tri_h+' l -'+tri_w+','+tri_h+' z ';
    })
    .style('fill','black')
    .style('opacity',0.5);

  // mouseover behavior
  d3.select('#play_button')
    .on('mouseover', function(){
      d3.select(this)
        .select('path')
        .style('fill','red')
        .style('opacity',1);

      d3.select(this)
        .select('circle')
        .style('opacity',1);

    })
    .on('mouseout', function(){
      d3.select(this)
        .select('path')
        .style('fill','black')
        .style('opacity',0.5);
      d3.select(this)
        .select('circle')
        .style('opacity',0.5);
    })
    .on('click', click_play)
        
}

var delay = {};
delay.reorder_title = 600;
delay.reorder = delay.reorder_title + 1000;
delay.read_duration = 1000;


function click_play(){

  // remove play button 
  d3.select(this)
    .transition().duration(500)
    .style('opacity',0);

  // show text 
  setTimeout(function(){

      if (cgm.params.zoom.scale() != 1){
        cgm.reset_zoom();
      }

      d3.select('#demo_text_box')
        .style('display','block')
        .transition().delay(delay.read_duration)
        .style('display','none');

    }, delay.reorder_title );

  setTimeout( function(){
    cgm.reorder('rank','row');
  }, delay.reorder );


}

