function answerSelected() {
    let res = false;
    $('.answer-option').each(function (i, obj) {
        res = res || $(this).hasClass("selected-answer");
    });

    return res;
}

function shuffle(array) {
    let currentIndex = array.length;
    while (currentIndex != 0) {
        let randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex--;
        [array[currentIndex], array[randomIndex]] = [array[randomIndex], array[currentIndex]];
    }
}

function generateImagePositions() {
    let allQs = question.body.correct.concat(question.body.incorrect);
    shuffle(allQs);
    $('.answer-col').each(function (i, obj) {
        let img = $(`<img class="answer-option" src="../static/images/${allQs[i]}"${question.body.correct.includes(allQs[i]) ? "data-correct" : ""}/>`)
        $(this).append(img);
    });
}

function isResultScreen() {
    return $('.answer-option').length == 0;
}

function isNextDisabled() {
    // no answer options = we are on a result screen
    if (isResultScreen()) {
        return false;
    }

    // TODO: incorporate checks on other question formats
    return !answerSelected();
}

function nextQuestion() {
    if (question.id < 4) {
        window.location.href = `/quiz/${question.id + 1}`;
    } else {
        window.location.href = "/result";
    }
}

function displayAnswerResults() {
    let score = 0;
    $('.answer-option').each(function (i, obj) {
        $(this).removeClass("answer-option");
        if (typeof $(this).attr("data-correct") !== 'undefined') {
            if ($(this).hasClass("selected-answer")) {
                score++;
            }
            $(this).addClass("correct-answer");
        } else if ($(this).hasClass("selected-answer")) {
            score--;
            $(this).addClass("incorrect-answer");
        }
    });
    score = Math.max(score, 0);
    sendScore(score, 2);
}

function sendScore(score, maxScore) {
    let data = {
        'score': score,
        'maxScore': maxScore
    };
    $.ajax({
        type: "POST",
        url: "/updateScore",
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
    // on startup
    generateImagePositions();
    $("#next-btn").prop("disabled", isNextDisabled());

    // // go to previous page or go back to the home page
    // $("#back-btn").click(function () {
    //     if (question.id > 0) {
    //         window.location.href = `/quiz/${question.id - 1}`;
    //     } else {
    //         window.location.href = "/";
    //     }
    // });

    $("#next-btn").click(function () {
        if (isResultScreen()) {
            nextQuestion();
        } else {
            displayAnswerResults();
        }
    });

    $(".answer-option").click(function () {
        // highlight/unhighlight selected answer
        $(this).toggleClass("selected-answer");

        // if any answer is selected, enable the next button
        $("#next-btn").prop("disabled", isNextDisabled());
    });
})