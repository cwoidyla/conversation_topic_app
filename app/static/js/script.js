function generateGraph(topic) {
    fetch("/get_associated_topics", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ topic: topic }),
    })
    .then(response => response.json())
    .then(data => {
        // Use D3.js or any other visualization library to generate the graph using 'data.topics'
        // Add event listeners to new nodes to make them clickable.
        // For simplicity, the D3.js implementation isn't detailed here.
    })
    .catch(error => console.error("Error:", error));
}

document.querySelector("#generateButton").addEventListener("click", function() {
    const topic = document.querySelector("#inputTopic").value;
    generateGraph(topic);
});

