document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("cloneForm");

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const checkboxes = document.querySelectorAll('input[name="servers"]:checked');
        const selected = Array.from(checkboxes).map(cb => cb.value);

        if (selected.length === 0) {
            alert("Please select at least one server to start cloning.");
            return;
        }

        fetch("/start-multiple", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ servers: selected })
        })
        .then(response => response.json())
        .then(data => {
            selected.forEach(server => {
                // Start polling status for each selected server
                pollStatus(server);
            });
        })
        .catch(error => {
            console.error("Error starting clone:", error);
        });
    });

    function pollStatus(server) {
        const progressFill = document.getElementById(`progress-${server}`);
        const statusCell = document.querySelector(`tr[data-server="${server}"] .status`);

        const interval = setInterval(() => {
            fetch(`/status/${server}`)
                .then(res => res.json())
                .then(data => {
                    const status = data.status || "Idle";

                    // Optional crude % estimate if byte count is being parsed
                    let progress = 0;
                    if (data.progress && data.progress > 0) {
                        // Rough estimate: assume source disk is 512GB
                        progress = Math.min(100, Math.floor((data.progress / (512 * 1024 ** 3)) * 100));
                    }

                    progressFill.style.width = progress + "%";
                    statusCell.textContent = status;

                    if (status === "SUCCESS") {
                        statusCell.className = "status success";
                        clearInterval(interval);
                        progressFill.style.width = "100%";
                    } else if (status === "FAILURE") {
                        statusCell.className = "status failure";
                        clearInterval(interval);
                    } else if (status === "RUNNING") {
                        statusCell.className = "status running";
                    } else {
                        clearInterval(interval);
                    }
                })
                .catch(err => {
                    console.error(`Error polling ${server}:`, err);
                    clearInterval(interval);
                });
        }, 3000); // Poll every 3 seconds
    }
});
