let isResultScreen = false;

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
        let img = $(`<img class="image-select answer-option" src="../static/images/${allQs[i]}"${question.body.correct.includes(allQs[i]) ? "data-correct" : ""}/>`)
        $(this).append(img);
    });
}

function loadQuestion() {
    switch(question.question_type) {
        case "select_images":
            generateImagePositions();
            break;
        case "dropdowns":
            break;
        default:

    }
}

function answerSelected() {
    let res = false;

    switch (question.question_type) {
        case "select_images":
            $('.answer-option').each(function (i, obj) {
                res = res || $(this).hasClass("selected-answer");
            });
            break;
        case "dropdowns":
            res = true;
            break;
    }

    return res;
}

function displayAnswerResults() {
    let score = 0;
    switch (question.question_type) {
        case "select_images":
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
            break;
        case "dropdowns":
            console.log(question.body.left);
            console.log($("#left-dropdown").find(":selected").val());

            if (question.body.left.includes($("#left-dropdown").find(":selected").val())) {
                $("#left-dropdown").addClass("correct-answer");
                score++;
            } else {
                $("#left-dropdown").addClass("incorrect-answer");
                let feedback = `Correct answers: ${question.body.left.join(", ")}`;
                $("#left-feedback").html(feedback);
            }
            if (question.body.right.includes($("#right-dropdown").find(":selected").val())) {
                $("#right-dropdown").addClass("correct-answer");
                score++;
            } else {
                $("#right-dropdown").addClass("incorrect-answer");
                let feedback = `Correct answers: ${question.body.right.join(", ")}`;
                $("#right-feedback").html(feedback);
            }
            break;
        default:
    }
    sendScore(score, 2);
}

function isNextDisabled() {
    if (isResultScreen) {
        return false;
    }

    return !answerSelected();
}

function nextQuestion() {
    if (question.id < num_questions - 1) {
        window.location.href = `/quiz/${question.id + 1}`;
    } else {
        window.location.href = "/result";
    }
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
    loadQuestion();

    // Handle click event on the 'Next' button
    $("#next-btn").click(function () {
        if (!isResultScreen && !answerSelected()) {
            // Display the error message if no answer is selected
            $("#error-message").show();
        } else {
            // Proceed as normal if an answer is selected
            $("#error-message").hide(); // Hide error message in case it was shown previously
            if (isResultScreen) {
                nextQuestion();
            } else {
                displayAnswerResults();
                isResultScreen = !isResultScreen;
            }
        }
    });

    // Handle click event on answer options
    $(".answer-option").click(function () {
        $(this).toggleClass("selected-answer");
        
        // Optionally update the button's enabled state
        // (You can also remove this if you want the button always enabled)
        $("#next-btn").prop("disabled", false);
        
        // Hide error message when an answer is selected
        if (answerSelected()) {
            $("#error-message").hide();
        }
    });
});

function answerSelected() {
    let selected = false;
    switch (question.question_type) {
        case "select_images":
            $('.answer-option').each(function () {
                if ($(this).hasClass("selected-answer")) selected = true;
            });
            break;
        case "dropdowns":
            selected = $("#left-dropdown").val() !== "" && $("#right-dropdown").val() !== "";
            break;
    }
    return selected;
}