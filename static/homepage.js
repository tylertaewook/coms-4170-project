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

$(document).ready(function () {
    $("#learn-btn").click(function () {
        window.location.href = "/lesson/0";
    });
    $("#quiz-btn").click(function () {
        resetScore();
        window.location.href = "/quiz/0";
    });
})