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

function sendScore(score, maxScore, timeTaken) {
    clearInterval(timerInterval);
    timeTaken = elapsedTime;
    
    let data = {
        'score': score,
        'maxScore': maxScore,
        'timeTaken': timeTaken
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

// For timer 
let startTime;
let elapsedTime = 0;
let timerInterval; 

function timeToString(time) {
    let diffInHrs = time / 3600000;
    let hh = Math.floor(diffInHrs);
  
    let diffInMin = (diffInHrs - hh) * 60;
    let mm = Math.floor(diffInMin);
  
    let diffInSec = (diffInMin - mm) * 60;
    let ss = Math.floor(diffInSec);
  
    let formattedHH = hh.toString().padStart(2, "0");
    let formattedMM = mm.toString().padStart(2, "0");
    let formattedSS = ss.toString().padStart(2, "0");
  
    return `${formattedHH}:${formattedMM}:${formattedSS}`;
}

function startTimer() {
    startTime = Date.now() - elapsedTime;
    timerInterval = setInterval(function printTime() {
      elapsedTime = Date.now() - startTime;
      document.getElementById("displayTimer").innerHTML = timeToString(elapsedTime);
    }, 1000);
  }

document.addEventListener("DOMContentLoaded", function() {
    startTimer();
});


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