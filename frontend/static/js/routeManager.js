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