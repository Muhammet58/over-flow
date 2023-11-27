function toggleIncrease(question_id) {
    var vote_text = document.getElementById("voteText" + question_id);

    $.ajax({
        type: "GET",
        url: "/increase/" + question_id,
        dataType: "json",
        success: function (response) {
            vote_text.innerText = response.increase_vote;
        },
        error: function () {
            alert("Hata oluştu !");
        },
    });
};



function toggleDecrease(question_id) {
    var vote_text = document.getElementById("voteText" + question_id);

    $.ajax({
        type: "GET",
        url: "/decrease/" + question_id,
        dataType: "json",
        success: function (response) {
            vote_text.innerText = response.decrease_vote;
        },
        error: function () {
            alert("Hata oluştu !");
        },
    });
};
