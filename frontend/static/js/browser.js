function addRedirect(name) {
    if (name in mapping.points)
        window.location.href = "/point/" + mapping.points[name];
    else
        window.location.href = "/segment/" + mapping.segments[name];
}

$( function() {
    $( "#tags" ).autocomplete({
      source: names,
      minLength: 3,
      select: function (event, selection) {
          addRedirect(selection.item.value)
      }
        });
    });

    const node = document.getElementById("tags")
    node.addEventListener("keydown", function(event) {
    if (event.key === "Enter")
        addRedirect(node.value)

});