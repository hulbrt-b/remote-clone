document.getElementById("startForm").onsubmit = function(e) {
    e.preventDefault();
    const form = new FormData(e.target);
    fetch('/start', {
        method: 'POST',
        body: form
    }).then(resp => resp.json())
      .then(data => {
          const taskId = data.task_id;
          checkStatus(taskId);
      });
};

function checkStatus(taskId) {
    const interval = setInterval(() => {
        fetch(`/status/${taskId}`)
            .then(resp => resp.json())
            .then(data => {
                document.getElementById('progress').innerText = data.status;
                if (data.status === 'SUCCESS' || data.status === 'FAILURE') {
                    clearInterval(interval);
                    location.reload();  // Reload to update history
                }
            });
    }, 2000);
}

