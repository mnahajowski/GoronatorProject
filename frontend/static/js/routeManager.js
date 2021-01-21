function verification() {
    // send to verification
    document.getElementById('verification-icon').setAttribute('src', '/static/images/share-icon-grey.svg')
    document.getElementById('verification-icon').style.cursor = 'default'
    document.getElementById('verification-icon').onclick = () => false
}

function deleteRoute(tourist_id, route_id) {
    const url = `http://localhost:5001/delete_route/${route_id}`;
    const payload = {
        mode: 'no-cors',
        method: "POST"
    };

    fetch(url, payload)
        .then(res => {
            redirect()
        })

    function redirect() {
        window.location.href = `/routes/${tourist_id}`
    }
}