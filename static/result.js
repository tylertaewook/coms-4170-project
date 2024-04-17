function resetScore() {
    let data = {
    };
    $.ajax({
        type: "POST",
        url: "/resetScore",
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(data),
        success: function (response) {
            console.log(response);
        },
        error: function (request, status, error) {
            console.log("Error");
            console.log(request);
            console.log(status);
            console.log(error);
        }
    });
}
// Display time 
//document.getElementById("displayTime").innerHTML = timeToString(yourTimeData);



$(document).ready(function () {
    $("#home-btn").click(function () {
        window.location.href = "/";
    });
    $("#retry-btn").click(function () {
        resetScore();
        window.location.href = "/quiz/0";
    });
})