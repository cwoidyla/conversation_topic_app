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
    // D3.js graph drawing logic goes here
}
