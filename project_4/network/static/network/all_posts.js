document.addEventListener('DOMContentLoaded', function() {
    
    document.querySelector('#test-button').onclick = function () {
        this.style.backgroundColor = 'blue';
    }

    // like button via javascript route
    document.querySelector('#like-button').onclick = function () {
        
        fetch(`/likes`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            }})
        .then(response => response.json())
        .then(result => {
            if (result.message) {
                console.log(result.message);
            } else {
                console.log("route failed. Investigate.")
            }

            document.querySelector('#total-likes').innerHTML = result.id;
        });
    }
});