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
    let allQs = lesson.body.correct.concat(lesson.body.incorrect);
    shuffle(allQs);
    $('.answer-col').each(function (i, obj) {
        let img = $(`<img class="answer-option" src="../static/images/${allQs[i]}"${lesson.body.correct.includes(allQs[i]) ? "data-correct" : ""}/>`)
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

function nextLesson() {
    if (lesson.id < 9) {
        window.location.href = `/lesson/${lesson.id + 1}`;
    } else {
        window.location.href = "/";
    }
}

function displayAnswerResults() {
    $('.answer-option').each(function (i, obj) {
        $(this).removeClass("answer-option");
        if (typeof $(this).attr("data-correct") !== 'undefined') {
            $(this).addClass("correct-answer");
        } else if ($(this).hasClass("selected-answer")) {
            $(this).addClass("incorrect-answer");
        }
    });
}

$(document).ready(function () {
    // on startup
    $("#next-btn").prop("disabled", isNextDisabled());
    if (lesson.lesson_type == "question") {
        generateImagePositions();
    }

    // go to previous lesson page or go back to the home page
    $("#back-btn").click(function () {
        if (lesson.id > 0) {
            window.location.href = `/lesson/${lesson.id - 1}`;
        } else {
            window.location.href = "/";
        }
    });

    $("#next-btn").click(function () {
        if (lesson.lesson_type == "explain") {
            nextLesson();
        } else {
            if (isResultScreen()) {
                nextLesson();
            } else {
                displayAnswerResults();
            }
        }
    });

    $(".answer-option").click(function () {
        // highlight/unhighlight selected answer
        $(this).toggleClass("selected-answer");

        // if any answer is selected, enable the next button
        $("#next-btn").prop("disabled", isNextDisabled());
    });
})