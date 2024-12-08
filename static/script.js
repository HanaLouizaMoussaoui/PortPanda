


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
        }
