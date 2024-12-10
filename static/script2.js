

    function displayResults() {
    const results = [
        { port: 80, protocol: "TCP", state: "open", service: "http" },
        { port: 443, protocol: "TCP", state: "open", service: "https" },
        { port: 22, protocol: "TCP", state: "closed" },
        { port: 23, protocol: "TCP", state: "closed" },
        { port: 25, protocol: "TCP", state: "closed" },
    ];
        const summaryElement = document.getElementById("summary");
        const detailsElement = document.getElementById("details");

        let closedTcpCount = 0;
        let openPorts = [];

        results.forEach(result => {
            if (result.protocol === "TCP" && result.state === "closed") {
                closedTcpCount++;
            } else {
                openPorts.push(result);
            }
        });

        if (closedTcpCount > 0) {
            const closedSummary = document.createElement("p");
            closedSummary.textContent = `${closedTcpCount} closed TCP ports`;
            summaryElement.appendChild(closedSummary);
        }

        openPorts.forEach(result => {
            const listItem = document.createElement("li");
            listItem.textContent = `Port ${result.port} (${result.protocol}): ${result.state} - ${result.service || "unknown service"}`;
            detailsElement.appendChild(listItem);
        });
    }

    //displayResults()