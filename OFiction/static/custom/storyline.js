$(function () {
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
});