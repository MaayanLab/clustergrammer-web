
// change the zscore cutoff 
function change_zscore_clustergram(inst_zscore_cutoff){

	// make new clustergram 
	///////////////////////////
	load_new_clustergram('svg_div_exp');

};

function load_new_clustergram(network){

	// pass the network data to d3_clustergram 
	make_d3_clustergram(network);

	// generate a list of genes for auto complete 
	////////////////////////////////////////////////
	// get all genes 
	all_genes = [];

	// loop through row_nodes
	for (i=0; i<row_nodes.length; i++){
		all_genes.push( row_nodes[i]['name'] ); 
	};

	// use Jquery autocomplete
	////////////////////////////////
  $( "#gene_search_box" ).autocomplete({
    source: all_genes
  });


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

