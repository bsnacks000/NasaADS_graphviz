
var forceAtlasConfig = {
    linLogMode: false,
    outboundAttractionDistribution: true,
    //barnesHutOptimize: true,
    startingIterations: 12, // maybe figure out how to scale these for size of graph
    iterationsPerRender: 12,
    gravity:2.25
    //edgeWeightInfluence: 0.1 //maybe mess with this value for subgraphs
}

$(document).ready(function(){

    $(".form-inline").on("submit", function(event){

        $.ajax({
            data : {
                query : $("#querySelect").val(),
                gtype : $("#gtypeSelect").val()
            },
            type : 'POST',
            url : '/make_graph',
            success: function(graph_data){
                if (!graph_data.error){
                    $("#graphContainer").empty(); // clear container of previous graph
                    $("#controlContainer").css('visibility','visible')

                    var s = make_graph(graph_data);
                    s.startForceAtlas2(forceAtlasConfig);

                    $("#pauseForceAtlas").on('click', function(event){
                        if (s.isForceAtlas2Running())
                            s.stopForceAtlas2();
                        else
                            s.startForceAtlas2();
                    });
                }
            }
        });

        event.preventDefault();
    });
});

// from the sigmajs documentation...
// adds neighbors method to sigma factory class -> populates allNeighborsIndex
sigma.classes.graph.addMethod('neighbors', function(nodeId) {
   var k;
   var neighbors = {};
   var index = this.allNeighborsIndex[nodeId] || {};

   for (k in index)
     neighbors[k] = this.nodesIndex[k];

   return neighbors;
 });



//generate graph with sigma
// added onClick functionality for nearest neighbors
function make_graph(graph_data){

    var s = new sigma({
            graph: graph_data,
            container: 'graphContainer',
            renderer: {
                container: document.getElementById('graphContainer'),
                type: 'canvas'
            },
            settings: {
              drawEdges: true,
              drawLabels: false,
              //defaultEdgeColor: '#d3d3d3',
              //edgeColor: 'default'
            }
        });

    // binding events for neighbors
    s.graph.nodes().forEach(function(n) {
        n.originalColor = n.color;
    });

    s.graph.edges().forEach(function(e) {
        e.originalColor = e.color;
    });


    s.bind('clickNode', function(e) {
        var nodeId = e.data.node.id;
        var toKeep = s.graph.neighbors(nodeId);

        toKeep[nodeId] = e.data.node;

        s.graph.nodes().forEach(function(n) {
          if (toKeep[n.id])
            n.color = n.originalColor;
          else
            n.color = '#eee';
        });

        s.graph.edges().forEach(function(e) {
          if (toKeep[e.source] && toKeep[e.target])
            e.color = e.originalColor;
          else
            e.color = '#eee';
        });

        // Since the data has been modified, we need to
        // call the refresh method to make the colors
        // update effective.
        s.refresh();
    });

    s.bind('clickStage', function(e) {
        s.graph.nodes().forEach(function(n) {
          n.color = n.originalColor;
        });

        s.graph.edges().forEach(function(e) {
          e.color = e.originalColor;
        });

        // Same as in the previous event:
        s.refresh();
    });

    //s.startForceAtlas2(config);
    return s;
}


/*
linLogMode: boolean false
outboundAttractionDistribution boolean false
adjustSizes boolean false
edgeWeightInfluence number 0
scalingRatio number 1
strongGravityMode boolean false
gravity number 1
barnesHutOptimize boolean true: should we use the algorithm's Barnes-Hut to improve repulsion's scalability (O(n²) to O(nlog(n)))? This is useful for large graph but harmful to small ones.
barnesHutTheta number 0.5
slowDown number 1
startingIterations integer 1: number of iterations to be run before the first render.
iterationsPerRender integer 1: number of iterations to be run before each render.

*/
