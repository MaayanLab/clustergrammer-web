function load_viz_new(network_data){

  var outer_margins = {
      'top':5,
      'bottom':5,
      'left':195,
      'right':2
    };

  var viz_size = {
    'width':1000,
    'height':600
  };

  about_string = 'Enriched Terms are the columns, input genes are the rows, and cells in the matrix indicate if a gene is associated with a term.';

  // define arguments object
  var arguments_obj = {
    root: '#container-id-1',
    'network_data': network_data,
    'row_label':'Input Genes',
    'col_label':'Enriched Terms',
    'outer_margins': outer_margins,
    // 'outline_colors':['black','yellow'],
    // 'tile_click_hlight':true,
    'show_label_tooltips':true,
    // 'show_tile_tooltips':true,
    // 'make_tile_tooltip':make_tile_tooltip,
    // 'highlight_color':'yellow',
    // 'super_label_scale':1.25,
    // 'transpose':true,
    // 'ini_expand':true,
    // 'col_label_scale':1.5,
    // 'row_label_scale':0.8
    // 'force_square':1
    // 'opacity_scale':'log',
    // 'input_domain':2,
    // 'do_zoom':false,
    // 'tile_colors':['#ED9124','#1C86EE'],
    'bar_colors':['#ff6666','#1C86EE'],
    'tile_colors':['#ff6666','#1C86EE'],
    // 'background_color':'orange',
    // 'tile_title': true,
    // 'click_group': click_group_callback,
    // 'size':viz_size
    // 'order':'rank'
    // 'row_order':'clust'
    'col_order':'rank',
    'ini_view':{'N_row_sum':'25', 'N_col_sum':'10'},
    // 'current_col_cat':'category-one'
    // 'title':'Clustergrammer',
    'about':about_string,
    'sidebar_width':150,
    'row_search_placeholder':'Gene'
  };

  cgm = Clustergrammer(arguments_obj);

  _.each(['row','col'], function(inst_rc){

    d3.select('.toggle_'+inst_rc+'_order')
      .classed('btn-group-vertical',false)
      .classed('btn-group',true)
      .selectAll('button')
      .style('width','68px')
      .text(function(){
        var inst_text = d3.select(this).text();
        inst_text = inst_text.replace('Rank by','');
        return inst_text;
      });

    d3.select('.toggle_'+inst_rc+'_order')

  });

  d3.select('.submit_gene_button')
    .style('padding-top','7px');

  d3.select('.gene_search_box')
    .style('width','65px');

  d3.selectAll('.btn')
    .style('padding-top','3px')
    .style('padding-bottom','3px');

  d3.select('.submit_gene_button')
    .style('height','33px');

  d3.select('.sidebar_wrapper')
    .style('width','145px')
    .style('margin-left','1px');


  // arguments_obj.root = '#container-id-2';

  // cgm = Clustergrammer(arguments_obj);

  d3.select(cgm.params.root + ' .wait_message').remove();

}