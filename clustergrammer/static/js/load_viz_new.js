function load_viz_new(network_data){

  var outer_margins = {
      'top':5,
      'bottom':5,
      'left':195,
      'right':2
    };

  var outer_margins_expand = {
      'top':5,
      'bottom':5,
      'left':5, 
      'right':2
    };

  var viz_size = {
    'width':1000,
    'height':600
  };

  about_string = 'Enriched Terms are the columns, input genes are the rows, adn cells in the matrix indicate if a gene is associated with a term.';

  // define arguments object
  var arguments_obj = {
    root: '#container-id-1',
    'network_data': network_data,
    'row_label':'Row Title',
    'col_label':'Colum Title',
    'outer_margins': outer_margins,
    'outer_margins_expand': outer_margins_expand,
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
    'input_domain':2,
    // 'do_zoom':false,
    // 'tile_colors':['#ED9124','#1C86EE'],
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
    'about':about_string
  };

  cgm = Clustergrammer(arguments_obj);

  // arguments_obj.root = '#container-id-2';

  // cgm = Clustergrammer(arguments_obj);

  d3.select(cgm.params.root + ' .wait_message').remove();

}