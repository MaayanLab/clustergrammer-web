function load_viz_multiple_clust(network_data, network_sim_row, network_sim_col, 
  viz_id, viz_name){

  var tmp_num;
  var cat_colors;

  make_clust(network_data, make_sim_mats, network_sim_row, network_sim_col);

}

// make wait sign 
$.blockUI({ css: { 
    border: 'none', 
    padding: '15px', 
    backgroundColor: '#000', 
    '-webkit-border-radius': '10px', 
    '-moz-border-radius': '10px', 
    opacity: .8, 
    color: '#fff' 
} });

d3.select('.blockMsg').select('h1').text('Please wait...');

var viz_size = {'width':1140, 'height':750};

// define arguments object
var default_args = {
  'show_tile_tooltips':true,
  'about':'Zoom, scroll, and click buttons to interact with the clustergram.',
  'row_search_placeholder':'Gene'
};

// resize_container();

function make_clust(network_data, make_sim_mats, network_sim_row, network_sim_col){

  var args = $.extend(true, {}, default_args);
  args.root = '#container-id-1';
  args.network_data = network_data;

  cgm = Clustergrammer(args);
  d3.select(cgm.params.root+' .wait_message').remove();
  cat_colors = cgm.params.cat_colors;

  make_sim_mats(network_sim_col, 'col', cat_colors, unblock);
  make_sim_mats(network_sim_row, 'row', cat_colors, unblock);

  d3.select('#file_title')
    .html(viz_name);

  var fs_links = ['link_clust', 'link_sim_col', 'link_sim_row'];
  _.each(fs_links, function(inst_link){
    d3.select('#'+inst_link)
      .append('a')
      .attr('target', '_blank')
      .classed('blue_links', true)
      .attr('href',function(){
        var mat_type = '';
        if (inst_link === 'link_sim_col'){
          mat_type = 'sim_col:'
        } else if (inst_link === 'link_sim_row'){
          mat_type = 'sim_row:'
        }
        return 'viz/'+viz_id+'/'+mat_type+viz_name;
      })
      .html('View in full page')
      .style('margin-left', '1013px');
  });

}

function make_sim_mats(inst_network, inst_rc, cat_colors, unblock){

  clust_name = 'mult_view_sim_'+inst_rc+'.json'
  // d3.json('json/'+clust_name, function(network_data){

    var args = $.extend(true, {}, default_args);
    args.cat_colors = {};
    if (inst_rc === 'col'){
      tmp_num = 2;
      args.cat_colors.row = cat_colors.col;
      args.cat_colors.col = cat_colors.col;
    } else if (inst_rc === 'row'){
      tmp_num = 3;
      args.cat_colors.row = cat_colors.row;
      args.cat_colors.col = cat_colors.row;
    }

    args.root = '#container-id-'+tmp_num;

    args.network_data = inst_network;
    cgm = Clustergrammer(args);
    d3.select(cgm.params.root+' .wait_message').remove();
    unblock();
  // });

}

function unblock(){
  $.unblockUI();
}

function resize_container(){

  var screen_width = viz_size.width;
  var screen_height = viz_size.height;

  d3.selectAll('.clustergrammer_container')
    .style('width', screen_width+'px')
    .style('height', screen_height+'px');
}

window.onscroll = function() {

  var show_col_sim = 0;
  var show_row_sim = 1200;
  var hide_clust = 900;
  var hide_col_sim = 1800;
  var inst_scroll = $(document).scrollTop();

  // // load col sim mat 
  // if (inst_scroll > show_col_sim){
  //   if (d3.select('#container-id-2 .viz_svg').empty()){
  //     make_sim_mats('col', cat_colors)
  //   }
  // }

  // // load row sim mat 
  // if (inst_scroll > show_row_sim){
  //   if (d3.select('#container-id-3 .viz_svg').empty()){
  //     make_sim_mats('row', cat_colors)
  //   }
  // }

  // hide clust 
  if (inst_scroll > hide_clust){
    d3.select('#container-id-1 .viz_svg')
      .style('display', 'none');
  } else {
    d3.select('#container-id-1 .viz_svg')
      .style('display', 'block');
  }

  // hide col sim mat
  if (inst_scroll > hide_col_sim || inst_scroll < show_col_sim){
    d3.select('#container-id-2 .viz_svg')
      .style('display', 'none');
  } else {
    d3.select('#container-id-2 .viz_svg')
      .style('display', 'block');
  }

}

$(document).ready(function(){
    $(this).scrollTop(0);
});
