$( function() {
    $( "#autocomplete" ).autocomplete({
        source: "/address/outcode/",
        minLength: 2
    });
});

