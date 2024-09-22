document.getElementById('server-form').addEventListener('submit', function(e) {
    const serverInput = document.getElementById('server').value;
    if (!serverInput.startsWith('https://') && !serverInput.startsWith('http://')) {
        e.preventDefault();
        alert('Please enter a valid server URL starting with https:// or http://');
    }
});
