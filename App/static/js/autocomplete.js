$( function() {
    $( "#autocomplete" ).autocomplete({
        source: "/address/outcode/",
        minLength: 2,
        delay: 500,
        response: function (event, ui) {
            if (!ui.content.length) {
                let msg = {value:'', label:'No results found, try a different postcode'}
                ui.content.push(msg);
            }
        }
    });
});

