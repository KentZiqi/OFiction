$(document).ready(function () {
    var fiction_id = $('#fiction_id').text();

    function episodeInformation(id, summary) {
        return summary +
            "<div class='margin20'></div>" +
            "<a href='/episode/" + id + "'><div class='btn btn-default'>Read/Edit in episode view</div></a>" +
            "<div class='margin10'></div>" +
            "<a href='/episode/new/" + fiction_id + "/" + id + "'><div class='btn btn-default'>Evolve this episode</div></a>";
    }

    var cy = window.cy = cytoscape({
                                       container: document.getElementById('cy'),

                                       boxSelectionEnabled: false,
                                       autounselectify: true,

                                       layout: {
                                           name: 'dagre'
                                       },

                                       style: [
                                           {
                                               selector: 'node',
                                               style: {
                                                   'content': 'data(label)',
                                                   'text-valign': 'center',
                                                   'text-halign': 'right',
                                                   'background-color': '#4971b5',
                                                   'color': '#333',
                                                   'text-wrap': 'wrap',
                                                   'text-max-width': 160,
                                                   'shape': 'circle',
                                                   'width': 'data(popularity)',
                                                   'height': 'data(popularity)'
                                               }
                                           },

                                           {
                                               selector: 'edge',
                                               style: {
                                                   'width': 4,
                                                   'opacity': 0.4,
                                                   'target-arrow-shape': 'triangle',
                                                   'line-color': '#4971b5',
                                                   'target-arrow-color': '#4971b5'
                                               }
                                           }
                                       ]
                                   });

    function handle_node_hover() {
        cy.on('mouseover', 'node', function (event) {
            var node = event.cyTarget;
            var summary = node.attr('summary');
            node.qtip({
                          content: summary,
                          position: {
                              at: 'bottom center'
                          },
                          show: {
                              event: "mouseover",
                              solo: true,
                              ready: true
                          },
                          hide: {
                              event: 'mouseout'
                          },
                          style: {
                              classes: 'qtip-bootstrap',
                              tip: {
                                  width: 16,
                                  height: 8
                              }
                          }
                      }, event);
        });
    }

    function handle_nodes_creation(content) {
        var edge_list = [];
        jsonQ.each(content, function (key, value) {
            var node = {group: "nodes", data: {}};
            var id = value.id;
            node.data["id"] = value.id;
            node.data["label"] = value.title;
            node.data["summary"] = episodeInformation(id, value.summary);
            node.data["popularity"] = value.popularity * 5 + 15; // TODO: Improve algorithm relating bubble size to popularity
            cy.add(node);
            jsonQ.each(value.previous_ids_without_parent, function (key, value) {
                var edge = {group: "edges", data: {}};
                edge.data["source"] = value;
                edge.data["target"] = id;
                edge_list.push(edge);
            });
            jsonQ.each(value.next_ids_without_parent, function (key, value) {
                var edge = {group: "edges", data: {}};
                edge.data["source"] = id;
                edge.data["target"] = value;
                edge_list.push(edge);
            });
        });
        jsonQ.each(edge_list, function (key, value) {
            cy.add(value);
        });
    }

    $.ajax({url: "/api/fiction/" + fiction_id}).then(function (content) {
        handle_nodes_creation(content);
        cy.layout({name: "dagre"});
        handle_node_hover();
    }, function (xhr, status, error) {
        console.log(error);
    });
});