$(document).ready(function(){

    $("form").on("submit", function(event){

        $.ajax({
            data : {
                query : $("#querySelect").val(),
            },
            type : 'POST',
            url : '/make_graph',
        })
        .done(function(graph_data){

            $( "#graphContainer" ).empty(); // clear container of previous graph
            make_graph(graph_data)
        });

        // need to prevent default event behavior
        event.preventDefault();
    });
});

//generate graph with sigma
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
              defaultEdgeColor: '#d3d3d3',
              edgeColor: 'default'
            }
        });


    s.startForceAtlas2({
        linLogMode: false,
        outboundAttractionDistribution: true,
        //barnesHutOptimize: true,
        gravity:2
    });

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
