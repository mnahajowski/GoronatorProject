$( function() {
     console.log(myData);
    $( "#tags" ).autocomplete({
      source: myData
        });
    });


    const node = document.getElementById("tags")
    node.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        console.log(node.value);
    }
});