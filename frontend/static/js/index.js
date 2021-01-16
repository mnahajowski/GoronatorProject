$( function() {
    $( "#tags" ).autocomplete({
      source: names,
      minLength: 3,
      select: function (event, selection) {
          window.location.href = "/segment/" + mapping[selection.item.value];
      }
        });
    });

    const node = document.getElementById("tags")
    node.addEventListener("keydown", function(event) {
    if (event.key === "Enter")
        window.location.href = "/segment/" + mapping[node.value]

});