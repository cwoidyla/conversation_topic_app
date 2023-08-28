document.querySelector("#generateButton").addEventListener("click", function() {
    const startTopic = document.querySelector("#startTopic").value;
    const endTopic = document.querySelector("#endTopic").value;
    const numIntermediaries = document.querySelector("#numIntermediaries").value;
    
    fetch("/get_intermediary_topics", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ 
            start_topic: startTopic, 
            end_topic: endTopic, 
            num_intermediaries: numIntermediaries 
        }),
    })
    .then(response => response.json())
    .then(data => {
        drawGraph(data.topics);
    })
    .catch(error => console.error("Error:", error));
});

function drawGraph(topics) {
    // Clear the SVG
    d3.select("#graph").selectAll("*").remove();

    const svg = d3.select("#graph").append("svg")
                  .attr("width", "100%")
                  .attr("height", 500);

    // Create node objects from topics list of strings
    const nodes = topics.map(topic => ({ id: topic }));

    // Generate links between topics
    const links = nodes.slice(1).map((node, i) => ({ source: nodes[i].id, target: node.id }));

    // D3 force simulation setup
    const simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(d => d.id).distance(150))  // Increase link distance
    .force("charge", d3.forceManyBody().strength(-400))  // Increase repulsion strength
    .force("center", d3.forceCenter(window.innerWidth / 2, 250));

    const link = svg.selectAll("line")
                    .data(links)
                    .enter().append("line")
                    .attr("stroke", "blue");

    const node = svg.selectAll("circle")
                    .data(nodes)
                    .enter().append("circle")
                    .attr("r", 20)
                    .attr("fill", "white")
                    .attr("stroke", "black");

    const labels = svg.selectAll("text")
                      .data(nodes)
                      .enter().append("text")
                      .attr("dx", 15)
                      .attr("dy", ".35em")
                      .text(d => d.id);

    simulation.on("tick", () => {
        link.attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        node.attr("cx", d => d.x)
            .attr("cy", d => d.y);

        labels.attr("x", d => d.x)
              .attr("y", d => d.y);
    });
}
