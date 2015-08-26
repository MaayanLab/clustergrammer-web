
// change the zscore cutoff 
function change_zscore_clustergram(inst_zscore_cutoff){

	// make new clustergram 
	///////////////////////////
	load_new_clustergram('svg_div_exp');

};

function load_new_clustergram(network_data){

	console.log('in load new clustergram')

	// // pass the network data to d3_clustergram 
	// make_d3_clustergram(network);

	// define the outer margins of the visualization 
	var outer_margins = {
	    'top':7,
	    'bottom':32,
	    'left':200,
	    'right':30
	  };

	// define callback function for clicking on tile 
	function click_tile_callback(tile_info){
		console.log('my callback')
		console.log('clicking on ' + tile_info.row + ' row and ' + tile_info.col + ' col with value ' + String(tile_info.value))
	};

	// define callback function for clicking on group 
	function click_group_callback(group_info){
		console.log('running user defined click group callback')
		console.log(group_info.type);
		console.log(group_info.nodes);
		console.log(group_info.info);
	};

	// define arguments object 
	var arguments_obj = {
		'network_data': network_data,
		'svg_div_id': 'svg_div',
		// 'row_label':'Rows',
		// 'col_label':'Columns',
	  'outer_margins': outer_margins,
	  // 'input_domain':7,
	  'click_tile': click_tile_callback,
	  'click_group': click_group_callback,
	  'col_overflow':0.8
	  // 'resize':'no',
	  // 'order':'rank'
	};

	// make clustergram: pass network_data and the div name where the svg should be made 
	d3_clustergram.make_clust( arguments_obj );

	

}

// // submit genes button 
// $("#gene_search_box").keyup(function (e) {
//     if (e.keyCode == 13) {
//         // Do something
// 				// console.log('pressed enter');
// 				find_gene_in_clust();
//     }
// });

// // find gene in clustergram 
// function find_gene_in_clust(){
// 	// get the searched gene 
// 	search_gene = $('#gene_search_box').val();

// 	if (all_genes.indexOf(search_gene) != -1){
// 	  // zoom and highlight found gene 
// 	  /////////////////////////////////
// 	  zoom_and_highlight_found_gene(search_gene);
		
// 	};


// };

