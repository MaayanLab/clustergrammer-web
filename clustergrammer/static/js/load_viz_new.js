function load_viz_new(network_data){

  console.log('upating optional modules')

  var hzome = ini_hzome();

  var outer_margins = {
      'top':5,
      'bottom':30,
      'left':195,
      'right':2
    };

  var viz_size = {
    'width':1000,
    'height':600
  };

  var about_string = 'Zoom, scroll, and click buttons to interact with the clustergram. <a href="http://amp.pharm.mssm.edu/clustergrammer/help"> <i class="fa fa-question-circle" aria-hidden="true"></i> </a>';

  var args = {
    root: '#container-id-1',
    'network_data': network_data,
    'about':about_string,
    'row_tip_callback':hzome.gene_info,
    'dendro_callback':dendro_callback,
    'matrix_update_callback':matrix_update_callback,
    'sidebar_width':150,
  };


  resize_container(args);

  d3.select(window).on('resize',function(){
    resize_container();
    cgm.resize_viz();
  });

  cgm = Clustergrammer(args);

  d3.select(cgm.params.root + ' .wait_message').remove();

  // add clustergrammer logo
  d3.select(cgm.params.root+ ' .title_section')
    .append('a')
    .attr('href', '/clustergrammer/')
    .append('img')
    .classed('title_image',true)
    .attr('src','static/img/clustergrammer_logo.png')
    .attr('alt','clustergrammer')
    .style('width','145px')
    .style('margin-left','3px')
    .style('margin-top','5px');

  check_setup_enrichr(cgm);
}


function resize_container(args){

  var screen_width = window.innerWidth;
  var screen_height = window.innerHeight - 30;

  d3.select('#container-id-1')
    .style('width', screen_width+'px')
    .style('height', screen_height+'px');
}

function matrix_update_callback(){
  if (genes_were_found){
    enr_obj.clear_enrichr_results();
  }
}

function dendro_callback(inst_selection){

  var inst_rc;
  var inst_data = inst_selection.__data__;

  // toggle enrichr export section
  if (inst_data.inst_rc === 'row'){
    d3.select('.enrichr_export_section')
      .style('display', 'block');
  } else {
    d3.select('.enrichr_export_section')
      .style('display', 'none');
  }

}