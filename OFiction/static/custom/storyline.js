jsPlumb.ready(function () {

    var instance = jsPlumb.getInstance({Container: "canvas"});
    instance.connect({
                         source: "node-1",
                         target: "node-2",
                         paintStyle: {lineWidth: 4, strokeStyle: '#333'},
                         connector: "Straight",
                         anchors: ["Bottom", "Top"],
                         endpoint: "Blank",
                         endpointStyle: {fillStyle: "#333"}
                     })
    instance.connect({
                         source: "node-2",
                         target: "node-3",
                         paintStyle: {lineWidth: 4, strokeStyle: '#333'},
                         connector: "Straight",
                         anchors: ["Bottom", "Top"],
                         endpoint: "Blank",
                         endpointStyle: {fillStyle: "#333"}
                     })
    instance.connect({
                         source: "node-3",
                         target: "node-4",
                         paintStyle: {lineWidth: 4, strokeStyle: '#333'},
                         connector: "Straight",
                         anchors: ["Bottom", "Top"],
                         endpoint: "Blank",
                         endpointStyle: {fillStyle: "#333"}
                     })
    instance.connect({
                         source: "node-3",
                         target: "node-5",
                         paintStyle: {lineWidth: 4, strokeStyle: '#333'},
                         connector: "Straight",
                         anchors: ["Bottom", "Top"],
                         endpoint: "Blank",
                         endpointStyle: {fillStyle: "#333"}
                     })
    instance.connect({
                         source: "node-4",
                         target: "node-6",
                         paintStyle: {lineWidth: 4, strokeStyle: '#333'},
                         connector: "Straight",
                         anchors: ["Bottom", "Top"],
                         endpoint: "Blank",
                         endpointStyle: {fillStyle: "#333"}
                     })
    instance.connect({
                         source: "node-5",
                         target: "node-7",
                         paintStyle: {lineWidth: 4, strokeStyle: '#333'},
                         connector: "Straight",
                         anchors: ["Bottom", "Top"],
                         endpoint: "Blank",
                         endpointStyle: {fillStyle: "#333"}
                     })
});