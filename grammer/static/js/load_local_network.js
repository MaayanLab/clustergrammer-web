
// change the zscore cutoff 
function change_zscore_clustergram(inst_zscore_cutoff){

	// make new clustergram 
	///////////////////////////
	load_new_clustergram('svg_div_exp');

};

function load_new_clustergram(network){

	// // use d3 to load a json 
	// d3.json('/grammer/static/networks/example_network.json', function(network_data){

		// // make global copy of network_data 
		// global_network_data = network_data;

		// pass the network data to d3_clustergram 
		make_d3_clustergram(network);

	// });

}

// submit genes button 
$("#gene_search_box").keyup(function (e) {
    if (e.keyCode == 13) {
        // Do something
				// console.log('pressed enter');
				find_gene_in_clust();
    }
});

// find gene in clustergram 
function find_gene_in_clust(){
	// get the searched gene 
	search_gene = $('#gene_search_box').val();

	if (all_genes.indexOf(search_gene) != -1){
	  // zoom and highlight found gene 
	  /////////////////////////////////
	  zoom_and_highlight_found_gene(search_gene);
		
	};


};

