
function load_viz( viz_name, network_data ){

    $('#share_button').click(function() {
      $('#share_info').modal('toggle');
      $('#share_url').val(window.location.href);
    });


    $('#picture_button').click(function() {
      $('#picture_info').modal('toggle');
      // $('#share_url').val(window.location.href);
    });

    function QueryStringToJSON() { 
      var pairs = location.search.slice(1).split('&');
      
      var result = {};
      pairs.forEach(function(pair) {
          pair = pair.split('=');
          result[pair[0]] = decodeURIComponent(pair[1] || '');
      });

      return JSON.parse(JSON.stringify(result));
    }

    var query_string = QueryStringToJSON();

    var ini_expand;
    if (query_string.preview === 'true' ){
      d3.select('#clust_instruct_container')
        .style('display','none');
      ini_expand = true; 
    } else {
      d3.select('#clust_instruct_container')
        .style('display','block');
      ini_expand = false; 
    }

    if (query_string.row_label){
      var row_label = query_string.row_label;
    } else {
      var row_label = '';
    }

    if (query_string.col_label){
      var col_label = query_string.col_label;
    } else {
      var col_label = '';
    }

    var super_label_scale = 1.25;
    if (query_string.no_labels){
      super_label_scale = 0;
    }

    if (query_string.opacity_scale){
      var opacity_scale = query_string.opacity_scale;
    } else {
      var opacity_scale = 'linear';
    }

    if (query_string.order){
      var ini_order = query_string.order;
    } else {
      var ini_order = 'clust'
    }



    // fix depricated view names 
    _.each(network_data.views, function(d){
      if (_.has(d,'filt')){
        // rename 'filt' to 'filter_row_value'
        d.filter_row_value = d.filt;
      d3.select('#filter_title').remove();
      }
      if (_.has(d,'filter_row')){
        // rename 'filter_row' to 'filter_row_value'
        d.filter_row_value = d.filter_row;
      }      
    })

    // define the outer margins of the visualization
    var outer_margins = {
        'top':5 ,
        'bottom':33,
        'left':225,
        'right':5
      };

    var outer_margins_expand = {
        'top':5,
        'bottom':5,
        'left':5,
        'right':5
      };  

    // define callback function for clicking on tile
    function click_tile_callback(tile_info){
      console.log('my callback');
      console.log('clicking on ' + tile_info.row + ' row and ' + tile_info.col + ' col with value ' + String(tile_info.value))
    }

    // define callback function for clicking on group
    function click_group_callback(inst_rc, group_nodes_list){
      console.log('running user defined click group callback');

      $('#dendro_info').modal('toggle');
      d3.select('#dendro_info').select('.modal-body').select('p')
        .text(group_nodes_list.join('\t'));

      if (inst_rc==='row'){
        var type_title = 'Row';
      } else if (inst_rc==='col'){
        var type_title = 'Column';
      }

        
      d3.select('#dendro_info').select('.modal-title')
        .text(function(){
          return 'Selected '+type_title + ' Group';
        });


      options = {
        description:'some-description',
        list: group_nodes_list.join('\n')
      }

      // // send genes to Enrichr 
      // send_genes_to_enrichr(options);

    }



    // define arguments object
    var arguments_obj = {
      'network_data': network_data,
      'svg_div_id': 'svg_div',
      'col_label':col_label,
      'row_label':row_label,
      'outer_margins': outer_margins,
      'outer_margins_expand': outer_margins_expand,
      'show_label_tooltips':true,
      'ini_expand':ini_expand,  
      'super_label_scale':super_label_scale,
      // 'col_label_scale':1.2,
      'opacity_scale':opacity_scale,
      'order':ini_order,
    };


    // initialize filter value with querystring 
    if ( _.has(query_string,'filter_row_sum') ){
      // set this up: 'ini_view'
      arguments_obj.ini_view = { 'filter_row_sum' : query_string.filter_row_sum };
    }

    if ( _.has(query_string,'N_row_sum') ){
      // set this up: 'ini_view'
      arguments_obj.ini_view = { 'N_row_sum' : query_string.N_row_sum };
    }


    if (query_string.viz_type === 'enr_vect'){
      // show up/dn genes from enrichment 
      function make_tile_tooltip(d){
        // up and down 
        if ( d.info.up.length > 0 && d.info.dn.length > 0 ){
          var inst_up = 'Up Genes: '+ d.info.up.join('\t');
          var inst_dn = 'Down Genes: '+ d.info.dn.join('\t');
          var inst_string = "<p>"+inst_up+"</p>"+inst_dn;
          // improve
          var inst_score = Math.abs(d.value.toFixed(2));
        } else if ( d.info.up.length > 0 ){
          var inst_up = 'Up Genes: '+ d.info.up.join('\t');
          var inst_string = inst_up;
          var inst_score = d.value.toFixed(2);
        } else if ( d.info.dn.length > 0 ){
          var inst_dn = 'Down Genes: '+ d.info.dn.join('\t');
          var inst_string = inst_dn;
          var inst_score = -d.value.toFixed(2);
        }
        var inst_info = '<p>'+d.col_name+' is enriched for '+d.row_name+' with Combined Score: '+ inst_score +'</p>'
        return inst_info + inst_string; 
      }

      arguments_obj.make_tile_tooltip = make_tile_tooltip;
      arguments_obj.show_tile_tooltips = true;

    }

    if (query_string.viz_type === 'Enrichr_clustergram'){
      arguments_obj.col_label_scale = 1.25;
      arguments_obj.row_label_scale = 0.75;
      arguments_obj.row_label = 'Input Genes';
      arguments_obj.col_label = 'Enriched Terms';
    }

    if (ini_expand){
      d3.select('.footer_section').style('display','none');
    } else {
      d3.select('.footer_section').style('display','block');
    }


    if (network_data === 'processing'){
      d3.select('#wait_message').text('Processing... please wait a moment and refresh page.');
    } else if (network_data === 'error') {
      console.log('here')
      d3.select('#wait_message')
        .text('There was an error processing your matrix. Please re-check your data and try again.')
        .style('margin-left','30px');
    } else {

      if (_.has(network_data.row_nodes[0],'group')){
        arguments_obj.click_group = click_group_callback;
      }

      // make clustergram: pass network_data and the div name where the svg should be made
      d3.select('#wait_message').remove();
      var cgm = clustergrammer(arguments_obj);
    }

    
    // if (query_string.viz_type === 'Enrichr_clustergram'){
    //   d3.select('#expand_button').style('display','none');
    // }

    ini_sliders();

    // filter_row = _.filter(network_data.views, function(d){return _.has(d,'filter_row')});
    var filter_row_value = _.filter(network_data.views, function(d){return _.has(d,'filter_row_value')});
    var filter_row_num   = _.filter(network_data.views, function(d){return _.has(d,'filter_row_num')});
    var filter_row_sum   = _.filter(network_data.views, function(d){return _.has(d,'filter_row_sum')});
    var N_row_sum        = _.filter(network_data.views, function(d){return _.has(d,'N_row_sum')});



    if (_.has(network_data, 'views')){

      // filter based on single value 
      if (filter_row_value.length>0){
        set_up_filters('filter_row_value');
      } else {
        d3.selectAll('.filter_row_value').remove();
      }

      // filter row based on number of non-zero values 
      if (filter_row_num.length>0){
        set_up_filters('filter_row_num');
      } else {
        d3.selectAll('.filter_row_num').remove();
      }

      // filter row based on sum of row
      if (filter_row_sum.length>0){
        var inst_filter = 0;
        set_up_filters('filter_row_sum');
      } else {
        d3.selectAll('.filter_row_sum').remove();
      }

      // filter top N
      if (N_row_sum.length>0){
        // var inst_filter = 0;
        set_up_N_filters('N_row_sum');
      } else {
        d3.selectAll('.N_row_sum').remove();
      }

    } else {
      d3.select('#filter_title').remove();
      d3.selectAll('.filter_row_value').remove();
      d3.selectAll('.filter_row_num').remove();
      d3.selectAll('.filter_row_sum').remove();
      d3.selectAll('.N_row_sum').remove();
    }

    // set up ini view 
    if ( _.has(query_string,'filter_row_sum') ){
      inst_filter = query_string.filter_row_sum;
      // set up slider
      $('#slider_filter_row_sum').slider( "value", inst_filter*10);
      // set up slider title
      d3.select('#filter_row_sum').text('Filter Sum: '+inst_filter*100+'%');          
    }

    if ( _.has(query_string,'N_row_sum') ){
      inst_N = query_string.N_row_sum;

      // make N_dictionary 
      var N_dict = {};

      // filters
      var all_filt = _.pluck( network_data.views,'N_row_sum')

      _.each(all_filt, function(d){
        tmp_index = _.indexOf(all_filt, d)

        N_dict[tmp_index] = d;

      });      

      // get the index of the current requested value so that the slider can be
      // initialized 
      _.each(N_dict,function(d,i){
        if (String(d) === String(inst_N)){
          inst_index = i;
        }
      });

      // set up slider
      $('#slider_N_row_sum').slider( "value", inst_index);

      // set up slider title
      d3.select('#N_row_sum').text('Top rows:  '+inst_N+' rows');
    }    


    // save svg: example from: http://bl.ocks.org/pgiraud/8955139#profile.json
    ////////////////////////////////////////////////////////////////////////////
    function save_clust_svg(){

      d3.select('#expand_button').style('opacity',0);

      var html = d3.select("svg")
            .attr("title", "test2")
            .attr("version", 1.1)
            .attr("xmlns", "http://www.w3.org/2000/svg")
            .node().parentNode.innerHTML;        

      var blob = new Blob([html], {type: "image/svg+xml"});              

      saveAs(blob, "clustergrammer.svg");

      d3.select('#expand_button').style('opacity',0.4);
    }

    d3.select('#download_buttons')
      .append('p')
      .append('a')
      .html('Download SVG')
      .on('click',function(){
        save_clust_svg();
      });


    // save as PNG 
    /////////////////////////////////////////
    d3.select('#download_buttons')
      .append('p')
      .append('a')
      .html('Download PNG')
      .on('click',function(){
        d3.select('#expand_button').style('opacity',0);
        saveSvgAsPng(document.getElementById("main_svg"), "clustergrammer.png");
        d3.select('#expand_button').style('opacity',0.4);
      })


    function set_up_N_filters(filter_type){

      // filter 
      ////////////////////
      var views = network_data.views;
      var all_views = _.filter(views, function(d){return _.has(d,filter_type);});

      var inst_max = all_views.length - 1;

      // make N_dictionary 
      var N_dict = {};

      // filters
      var all_filt = _.pluck( network_data.views,'N_row_sum')

      _.each(all_filt, function(d){
        tmp_index = _.indexOf(all_filt, d)

        N_dict[tmp_index] = d;

      });


      $( '#slider_'+filter_type ).slider({
        value:0,
        min: 0,
        max: inst_max,
        step: 1,
        stop: function( event, ui ) {

          // change value 
          $( "#amount" ).val( "$" + ui.value );

          // get value 
          var inst_index = $( '#slider_'+filter_type ).slider( "value" ); 

          var inst_top = N_dict[inst_index];

          change_view = {'N_row_sum':inst_top};
          filter_name = 'N_row_sum';

          d3.select('#main_svg').style('opacity',0.70);

          d3.select('#'+filter_type).text('Top rows: '+inst_top+' rows'); 

          $('.slider_filter').slider('disable');
          d3.selectAll('.btn').attr('disabled',true);

          cgm.update_network(change_view);

          ini_sliders();

          function enable_slider(){
            $('.slider_filter').slider('enable');  
            d3.selectAll('.btn').attr('disabled',null);
          }
          setTimeout(enable_slider, 2500);

        }
      });
      $( "#amount" ).val( "$" + $( '#slider_'+filter_type ).slider( "value" ) );

    } 

    function set_up_filters(filter_type){

      console.log('filter_type: '+filter_type )

      // filter 
      ////////////////////
      var views = network_data.views;
      var all_views = _.filter(views, function(d){return _.has(d,filter_type);});
      var inst_max = all_views.length - 1;
      $( '#slider_'+filter_type ).slider({
        value:0,
        min: 0,
        max: inst_max,
        step: 1,
        stop: function( event, ui ) {

          $( "#amount" ).val( "$" + ui.value );
          var inst_filt = $( '#slider_'+filter_type ).slider( "value" ); 

          if (filter_type==='filter_row_value' || filter_type == 'filter_row'){

            change_view = {'filter_row_value':inst_filt/10};
            filter_name = 'Value';

            $('#slider_filter_row_sum').slider( "value", 0);
            $('#slider_filter_row_num').slider( "value", 0);

            d3.select('#filter_row_sum').text('Filter Sum: 0%');          
            d3.select('#filter_row_num').text('Filter Number Non-zero: 0%');          

          } else if (filter_type === 'filter_row_num'){

            change_view = {'filter_row_num':inst_filt/10};
            filter_name = 'Number Non-zero';

            $('#slider_filter_row_value').slider( "value", 0);
            $('#slider_filter_row_sum').slider( "value", 0);

            d3.select('#filter_row_sum').text('Filter Sum: 0%');          
            d3.select('#filter_row_value').text('Filter Value: 0%');          

          } else if (filter_type === 'filter_row_sum'){

            change_view = {'filter_row_sum':inst_filt/10};
            filter_name = 'Sum';

            $('#slider_filter_row_value').slider( "value", 0);
            $('#slider_filter_row_num').slider( "value", 0);

            d3.select('#filter_row_value').text('Filter Value: 0%');          
            d3.select('#filter_row_num').text('Filter Number Non-zero: 0%'); 

          }

          d3.select('#main_svg')
            .style('opacity',0.70);

          d3.select('#'+filter_type).text('Filter '+filter_name+': '+10*inst_filt+'%'); 
          $('.slider_filter').slider('disable');
          d3.selectAll('.btn').attr('disabled',true);

          cgm.update_network(change_view);

          ini_sliders();

          function enable_slider(){
            $('.slider_filter').slider('enable');  
            d3.selectAll('.btn').attr('disabled',null);
          }
          setTimeout(enable_slider, 2500);

        }
      });
      $( "#amount" ).val( "$" + $( '#slider_'+filter_type ).slider( "value" ) );

    }     

    function ini_sliders(){

      $( "#slider_col" ).slider({
        value:0.5,
        min: 0,
        max: 1,
        step: 0.1,
        slide: function( event, ui ) {
          $( "#amount" ).val( "$" + ui.value );
          var inst_index = ui.value*10;
          cgm.change_groups('col',inst_index)
        }
      });
      $( "#amount" ).val( "$" + $( "#slider_col" ).slider( "value" ) );

      $( "#slider_row" ).slider({
        value:0.5,
        min: 0,
        max: 1,
        step: 0.1,
        slide: function( event, ui ) {
          $( "#amount" ).val( "$" + ui.value );
          var inst_index = ui.value*10;
          cgm.change_groups('row',inst_index)
        }
      });
      $( "#amount" ).val( "$" + $( "#slider_row" ).slider( "value" ) );

      $('#gene_search_box').autocomplete({
        source: cgm.get_genes()
      });

      // submit genes button
      $('#gene_search_box').keyup(function(e) {
        if (e.keyCode === 13) {
          var search_gene = $('#gene_search_box').val();
          cgm.find_gene(search_gene);
        }
      });

      $('#submit_gene_button').click(function() {
        var gene = $('#gene_search_box').val();
        cgm.find_gene(gene);
      });

      $('#toggle_row_order .btn').off().click(function(evt) {
        var order_id = $(evt.target).attr('id').split('_')[0];
        cgm.reorder(order_id,'row');
      });

      $('#toggle_col_order .btn').off().click(function(evt) {
        var order_id = $(evt.target).attr('id').split('_')[0];
        cgm.reorder(order_id,'col');
      });

    }

  }