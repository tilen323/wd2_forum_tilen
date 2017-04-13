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
           alert("You shall not pass! You are a bot or very bad at math");
           e.preventDefault();
       }
    });
});

$(document).ready(function(){

    $("#topicTable").DataTable( {

        "language" : {
            "lengthMenu": "Display _MENU_ topics per page",
            "zeroRecords": "Nothing found - sorry"
        }
    });

    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });
});