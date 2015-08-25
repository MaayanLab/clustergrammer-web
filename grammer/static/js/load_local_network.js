// change the protein class 
function change_class_clustergram(inst_prot_class){

	// clear input search box 
	$('#gene_search_box').val('')

	// only make clustergram if its a new class
	if (inst_prot_class != ccle_params['gc'])	{

		// update request_json 
    ccle_params['gc'] = inst_prot_class;

    // make sure that the protein class has data from this 
    // zscore cutoff 
    if ( _.indexOf(missing_z[inst_prot_class], ccle_params['cutoff']*10) >= 0 ){

    	// subtract 5 from the first missing zscore 
    	// convert to zscore 
    	var good_zscore = missing_z[inst_prot_class][0] - 5;

    	// use different rules for all genes 
    	if (inst_prot_class == 'ALL'){
    		// default to 3.5 zscore 
    		good_zscore = 35;
    	};

    	// set the zscore cutoff in ccle_params
    	ccle_params['cutoff'] = good_zscore/10;

    	// set the appropriate zscore button to active 
    	////////////////////////////////////////////////
    	// reset all buttons to inactive state 
    	d3.selectAll('.z_button').attr('class','z_button btn btn-primary prot_class');
    	d3.select('#z_'+good_zscore).attr('class','active z_button btn btn-primary prot_class');

    };

		// make new expression clustergram 
		/////////////////////////////////////
		load_new_clustergram('svg_div_exp');

	};

	// set zscore restrictions 
	// reinitialize all buttons 
	d3.selectAll('.z_button').attr('disabled',null);
	// disable zscore buttons
	for (i=0; i<missing_z[inst_prot_class].length; i++){
		var disable_z = missing_z[inst_prot_class][i];
		d3.select('#z_'+disable_z)
			.attr('disabled','disabled')
	};

};

// change the zscore cutoff 
function change_zscore_clustergram(inst_zscore_cutoff){

	// update request_json 
  ccle_params['cutoff'] = inst_zscore_cutoff;

	// make new clustergram 
	///////////////////////////
	load_new_clustergram('svg_div_exp');

};

function load_tfsub_clustergram(){

		// set up wait message before request is made 
		$.blockUI({ css: { 
		        border: 'none', 
		        padding: '15px', 
		        backgroundColor: '#000', 
		        '-webkit-border-radius': '10px', 
		        '-moz-border-radius': '10px', 
		        opacity: .8, 
		        color: '#fff' 
		    } });

	// // use d3 to load a json 
	// d3.json('/grammer/static/networks/'+ccle_params['gc']+'_exp_std_'+ccle_params['cutoff']+'.json', function(network_data){

	// //!! temporary change to test tf correlated expression 
	// d3.json('/grammer/static/networks/tf_SMARCA4.json', function(network_data){

	//!! temporary change to test similarity matrix 
	d3.json('/grammer/static/networks/TF_sim_KIN_exp_std_2.json', function(network_data){

		// make global copy of network_data 
		global_network_data = network_data;
		// pass the network data to d3_clustergram 
		make_d3_clustergram(network_data);
	  // turn off the wait sign 
	  $.unblockUI();
	});

}

function load_new_clustergram(){

		// set up wait message before request is made 
		$.blockUI({ css: { 
		        border: 'none', 
		        padding: '15px', 
		        backgroundColor: '#000', 
		        '-webkit-border-radius': '10px', 
		        '-moz-border-radius': '10px', 
		        opacity: .8, 
		        color: '#fff' 
		    } });

	// use d3 to load a json 
	d3.json('/grammer/static/networks/'+ccle_params['gc'].toLowerCase()+'_exp_std_'+ccle_params['cutoff']+'.json', function(network_data){

	// //!! temporary change to test tf correlated expression 
	// d3.json('/grammer/static/networks/tf_TBX18.json', function(network_data){

		// make global copy of network_data 
		global_network_data = network_data;
		// pass the network data to d3_clustergram 
		make_d3_clustergram(network_data);
	  // turn off the wait sign 
	  $.unblockUI();
	});


}

function highlight_resource_types(){

	// This will set up the resource type color key 
	// and generate an array of genes for later use
	//////////////////////////////////////////////////////

	// res_hexcodes = ['#097054','#FFDE00','#6599FF','#FF9900','#834C24','#003366','#1F1209']
	
	res_hexcodes = ['#0000FF','#FF0000','#C0C0C0', '#FFA500'];

	// define cell line groups 
	all_groups = ['TF group 1','TF group 2','TF group 3'];

	// generate an object to associate group with color 
	res_color_dict = {};

	// initialize the cell line color associations
	blue_cl = ['H1437','H1792','HCC15','A549','H1944','H1299','H1355','H838','CAL-12T','H23','H460','H661'];
	red_cl = ['H441','HCC78','H1734','H2228','H1781','H1975','H358','HCC827','H1703','H2342','H1650','LOU-NH91'];
	grey_cl = ['CALU-3','H2405','H2106', 'HCC44','H1666'];
	orange_cl = [] //['HCC44','H1666'];

	for (i=0; i<col_nodes.length;i++){
		// add blue cell line 
		if ( $.inArray(col_nodes[i]['name'],blue_cl) > -1 ){
			res_color_dict[col_nodes[i]['name']]=res_hexcodes[0];
		};
		// add red cell line 
		if ( $.inArray(col_nodes[i]['name'],red_cl)  > -1 ){
			res_color_dict[col_nodes[i]['name']]=res_hexcodes[1];
		};
		// add grey cell line 
		if ( $.inArray(col_nodes[i]['name'],grey_cl)  > -1 ){
			res_color_dict[col_nodes[i]['name']]=res_hexcodes[2];
		};
		// add orange cell line 
		if ( $.inArray(col_nodes[i]['name'],orange_cl)  > -1 ){
			res_color_dict[col_nodes[i]['name']]=res_hexcodes[3];
		};
	}

	// define association between tf groups and colors 
	res_color_key = {}
	res_color_key['TF group 1'] = res_hexcodes[0];
	res_color_key['TF group 2'] = res_hexcodes[1];
	res_color_key['TF group 3'] = res_hexcodes[2];
	res_color_key['TF group 4'] = res_hexcodes[3];

	// add color key 
	////////////////////
	// add keys 
	key_divs = d3.select('#res_color_key_div')
		.selectAll('row')
		.data(all_groups)
		.enter()
		.append('row')
		.style('padding-top','15px');

	// add color 
	key_divs
		.append('div')
		.attr('class','col-xs-2')
		// get rid of excess padding 
		.style('padding-left','5px')
		.style('padding-right','0px')
		.style('padding-top','1px')
		.append('div')
		.style('width','12px')
		.style('height','12px')
		.style('background-color', function(d){

			return res_color_key[d];
		})

	// add names 
	key_divs
		.append('div')
		.attr('class','col-xs-10 res_names_in_key')
		.append('text')
		.text(function(d){ 
			inst_res = d.replace(/_/g, ' ');
			// inst_res = _(inst_res).capitalize();
			return inst_res ;
		})

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


};

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

