// main js page for sigma and ajax
// jquery page load and ajax request handler
// contains the make_graph sigma function

$(document).ready(function(){

    var forceAtlasConfig = {
        linLogMode: false,
        outboundAttractionDistribution: true,
        startingIterations: 12, // maybe figure out how to scale these for size of graph
        iterationsPerRender: 20,
        gravity:2.25
    }

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


    // main ajax request form
    $("#requestForm").on("submit", function(event){
        event.preventDefault();

        $.ajax({
            data : {
                query : $("#querySelect").val(),
                gtype : $("#gtypeSelect").val()
            },
            type : 'POST',
            url : '/make_graph',
            success: function(graph_data){

                if (!graph_data.error){

                    $("#graphContainer").empty()
                    $("#controlContainer").css('visibility','visible')

                    var s = make_graph(graph_data);
                    s.startForceAtlas2(forceAtlasConfig);


                    $("#pauseForceAtlas").on('click', function(event){
                        if (s.isForceAtlas2Running())
                            s.stopForceAtlas2();
                        else
                            s.startForceAtlas2();
                    });

                    // remove a row from the table - remove header if empty
                    $("#htmlTable").on('click','.rm-btn', function(event){
                        $(this).closest('tr').remove();
                        if ($('#htmlTable > tbody').is(':empty'))
                            $('#htmlTableWrapper').css('visibility','hidden');
                    });

                    $("#exportButton").on('click',function(event){
                        $("#htmlTable").tableToCSV();
                    });



                } // can add an else error message here
            }
        });
    });

    $('#aboutButton').on('click', function(event){
        if ($('#abstractWrapper').css('display') == 'none')
            $('#abstractWrapper').show(100);
        else
            $('#abstractWrapper').hide(100);
    });

    // make graph function

    function make_graph(graph_data){

        var s = new sigma({
                graph: graph_data.graph,
                container: 'graphContainer',
                renderers: [{
                    container: document.getElementById('graphContainer'),
                    type: 'canvas'
                }],
                settings: {
                  drawEdges: true,
                  drawLabels: false,
                  doubleClickEnabled: false
                }
            });

        // binding events for neighbors - save original color
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
                e.color = 'rgba(27, 115, 186, 0.90)';
              else
                e.color = 'rgba(1, 1, 1, 0.1)';
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

        // binding for html table
        s.bind('doubleClickNode', function(e){
            var data = {
                subject: "<td>"+graph_data.subject+"</td>",
                label: "<td>"+ e.data.node.label + "</td>",
                ntype: "<td>"+e.data.node.node_type + "</td>",
                betw: "<td>"+e.data.node.zbetween_central+ "</td>",
                deg: "<td>"+e.data.node.zdeg_central+ "</td>",
                pager:"<td>"+ e.data.node.zpagerank+ "</td>"
            };

            var removeButton = "<td><button type=button class='rm-btn'>remove</button><td>" ;

            // makes visible if hidden
            if ($('#htmlTable > tbody').is(':empty'))
                $('#htmlTableWrapper').css('visibility','visible');

            // append the node row
            $('#htmlTable > tbody').append(
                "<tr>"+data.label+data.subject+data.ntype+
                data.betw+data.deg+data.pager+removeButton+"</tr>"
            );
        });

        return s; // return the sigma instance to outer scope..
    }

});
