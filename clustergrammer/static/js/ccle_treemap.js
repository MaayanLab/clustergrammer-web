
console.log('making treemap')

var tree = {
    name: "tree",
    "children": [
    {
      "size": 12, 
      "name": "THYROID"
    }, 
    {
      "size": 2, 
      "name": "SALIVARY GLAND"
    }, 
    {
      "size": 21, 
      "name": "SOFT TISSUE"
    }, 
    {
      "size": 180, 
      "name": "HAEMATOPOIETIC AND LYMPHOID"
    }, 
    {
      "size": 8, 
      "name": "BILIARY TRACT"
    }, 
    {
      "size": 44, 
      "name": "PANCREAS"
    }, 
    {
      "size": 69, 
      "name": "CENTRAL NERVOUS SYSTEM"
    }, 
    {
      "size": 1, 
      "name": "SMALL INTESTINE"
    }, 
    {
      "size": 29, 
      "name": "BONE"
    }, 
    {
      "size": 61, 
      "name": "LARGE INTESTINE"
    }, 
    {
      "size": 17, 
      "name": "AUTONOMIC GANGLIA"
    }, 
    {
      "size": 11, 
      "name": "PLEURA"
    }, 
    {
      "size": 27, 
      "name": "URINARY TRACT"
    }, 
    {
      "size": 187, 
      "name": "LUNG"
    }, 
    {
      "size": 59, 
      "name": "BREAST"
    }, 
    {
      "size": 62, 
      "name": "SKIN"
    }, 
    {
      "size": 52, 
      "name": "OVARY"
    }, 
    {
      "size": 8, 
      "name": "PROSTATE"
    }, 
    {
      "size": 36, 
      "name": "KIDNEY"
    }, 
    {
      "size": 32, 
      "name": "UPPER AERODIGESTIVE TRACT"
    }, 
    {
      "size": 38, 
      "name": "STOMACH"
    }, 
    {
      "size": 27, 
      "name": "ENDOMETRIUM"
    }, 
    {
      "size": 26, 
      "name": "OESOPHAGUS"
    }, 
    {
      "size": 28, 
      "name": "LIVER"
    }
  ]
};

var width = 900, // innerWidth-40
    height = 700, // innerHeight-40,
    color = d3.scale.category20c(),
    div = d3.select("#tree_container").append("div")
       .attr('id','new_div')
       .style("position", "relative");

var treemap = d3.layout.treemap()
    .size([width, height])
    .sticky(true)
    .value(function(d) { return d.size; });

var tip = d3.tip()
  .attr('class', 'd3-tip')
  .direction('n')
  .offset([0, 0])
  .html('something');
 
var node = div.datum(tree).selectAll(".node")
      .data(treemap.nodes)
      .enter().append("div")
      .attr("class", "node")
      .on('click',function(d){
        console.log(d.size);
      })
      .attr('title', function(d) { return d.children ? null : d.name; })
      .call(position)
      .style("background-color", function(d) {
          return d.name == 'tree' ? '#fff' : color(d.name); })
      .append('div')
      .style("font-size", function(d) {
          // compute font size based on sqrt(area)
          return Math.max(15, 0.10*Math.sqrt(d.area))+'px'; })
      .text(function(d) { return d.children ? null : d.name; })

function position() {
  this.style("left", function(d) { return d.x + "px"; })
      .style("top", function(d) { return d.y + "px"; })
      .style("width", function(d) { return Math.max(0, d.dx - 1) + "px"; })
      .style("height", function(d) { return Math.max(0, d.dy - 1) + "px"; });
}
