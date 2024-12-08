




     function toggleSinglePort() {
            const singlePortCheckbox = document.getElementById('single-port');
            const startPortInput = document.getElementById('start-port');
            const startPortInputLabel = document.getElementById('start-port-label');
            const endPortInputLabel = document.getElementById('end-port-label');
            const endPortInput = document.getElementById('end-port');


            if (singlePortCheckbox.checked) {
                startPortInput.value = '';
                startPortInput.hidden = true;
                startPortInputLabel.textContent = "";
                endPortInputLabel.textContent = "Port"

                endPortInput.placeholder = "Enter single port";
            } else {
                startPortInput.hidden = false;
                startPortInputLabel.textContent = "Start Port";
                startPortInput.disabled = false;
                endPortInputLabel.textContent = "End Port"
                endPortInput.placeholder = "65535";
            }

              const scanResults = [
        { port: 80, protocol: "TCP", state: "open", service: "http" },
        { port: 443, protocol: "TCP", state: "open", service: "https" },
        { port: 22, protocol: "TCP", state: "closed" },
        { port: 23, protocol: "TCP", state: "closed" },
        { port: 25, protocol: "TCP", state: "closed" },
    ];

        }


