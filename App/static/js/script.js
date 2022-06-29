// Waits till the DOM  is ready for JS to be run
$(document).ready(function (){
    $('#full_postcode_data').hide();
    // When the search button is clicked the function is run
    $("#btn").click(function (){
        // Get postcode value from input field
        // $('#full_postcode_data').val('');
        let postcode = document.getElementById('autocomplete').value;
        $("option[id='added_option']").remove();
    // Holds the URL for the get API call
    let url = '/address/' + postcode;
        // Runs get request with users postcode
        $.get(url, function (data, status){
            console.log(`${status}`)
            // Loops through the returned object and outputs the gathered data
            $.each(data, function (key,value){
                $("#full_postcode_data").append($('<option/>', {
                    id: 'added_option',
                    value: value,
                    text: value
                }));
                console.log(key + ': ' + value + '\n')
                $('#full_postcode_data').show();
            });
        });
    });
});