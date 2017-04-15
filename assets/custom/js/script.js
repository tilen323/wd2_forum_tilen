/* Check if bot */

$(document).ready(function() {
    var numOne = Math.floor((Math.random() * 9) + 1);
    var numTwo = Math.floor((Math.random() * 9) + 1);
    var numSum = numOne + numTwo

    $("#create_topic_sum_label").text("What is the sum of " + numOne + " and " + numTwo + "?");

    var createTopicSum = $("#create_topic_sum");
    var createTopicBtn = $("#create_topic_btn");

    createTopicBtn.click(function(e) {
       if (createTopicSum.val() === numSum.toString()){
           createTopicBtn.hide().delay(2000).show(1);
           console.log("yaaay");
       }
       else {
           alert("You shall not pass! You are a bot or very bad at math :P");
           e.preventDefault();
       }
    });
});

$(document).ready(function(){

    $("#commentTable").DataTable( {

        "language" : {
            "lengthMenu": "",
            "zeroRecords": "Nothing found - sorry",
            "info": "Showing _START_ to _END_ of _TOTAL_ comments",
        },
        "dom" : "<fl<t>ip>",
        "order": [[ 2, "desc" ]]

    });

    $("#topicTable").DataTable( {

        "language" : {
            "lengthMenu": "Display _MENU_ topics per page",
            "zeroRecords": "Nothing found - sorry"
        },
        "order": [[ 3, "desc" ]]
    });

    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });
});