




     function toggleSinglePort() {
            const singlePortCheckbox = document.getElementById('single-port');
            const startPortInput = document.getElementById('start-port');
            const startPortInputLabel = document.getElementById('start-port-label');
            const endPortInputLabel = document.getElementById('end-port-label');
            const endPortInput = document.getElementById('end-port');


            if (singlePortCheckbox.checked) {
                startPortInput.hidden = true;
                startPortInput.value = '';
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



     document.addEventListener("DOMContentLoaded", function () {
        const form = document.querySelector("form");

        // This is to show the pop up before we trigger the scan
        if (form) {
            form.addEventListener("submit", function (event) {
                event.preventDefault();

                document.getElementById("loading-popup").style.display = "flex";

                setTimeout(() => {
                    form.submit();
                }, 100);
            });
        }
    });