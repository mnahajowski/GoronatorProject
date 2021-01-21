function updateRoute(route_id) {
    let route = getRouteData()

    const url = "http://localhost:5001/update_route/" + route_id;
    const payload = {
        headers: {
            "content-type": "application/json; charset=UTF-8",
        },
        mode: 'no-cors',
        body: JSON.stringify(route),
        method: "POST"
    };

    fetch(url, payload)
        .then(res => {
            window.alert("Successfully updated the route!")
        })
}
