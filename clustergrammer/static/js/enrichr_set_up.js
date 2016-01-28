function enrichr_set_up(cgm, network_data){

 /* 
  Make custom slider for Enrichr 
  */

  console.log('\n\nset up custom slider for Enrichr\n\n')

  // filter 
  ////////////////////
  var views = network_data.views;

  // gather N_row_sum views 
  var sub_views = _.filter(views, function(d){return _.has(d,'N_row_sum');});

  var inst_enr_type = 'combined_score';

  // gather enrichment type views 
  sub_views = _.filter(sub_views, 
    function(d){
      return d.enr_score_type == inst_enr_type;
    });

  console.log(sub_views)

  var inst_max = sub_views.length - 1;

  // make N_dictionary 
  var N_dict = {};

  // filters
  var all_filt = _.pluck( sub_views,'N_row_sum')

  _.each(all_filt, function(d){
    tmp_index = _.indexOf(all_filt, d)

    N_dict[tmp_index] = d;

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

  query_string = QueryStringToJSON();


  var filter_type = 'N_row_sum_enr';

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

      // ini_sliders();

      function enable_slider(){
        $('.slider_filter').slider('enable');  
        d3.selectAll('.btn').attr('disabled',null);
      }
      setTimeout(enable_slider, 2500);

    }
  });
  $( "#amount" ).val( "$" + $( '#slider_'+filter_type ).slider( "value" ) );

}