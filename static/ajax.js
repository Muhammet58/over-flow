function toggleQuestionVote(question_id, vote_type) {
    const vote_text = document.getElementById("voteText" + question_id);

    $.ajax({
        type: "GET",
        url:"/question-vote-ajax/" + question_id,
        dataType: "json",
        data: {"vote_type": vote_type},
        success: function (response) {
            vote_text.innerText = response.vote_count;
        },
        error: function () {
            alert("Hata oluştu !");
        },
    });
}



function toggleAnswerVote (answer_id, vote_type) {
    const vote_text = document.getElementById("answerVoteText" + answer_id);

    $.ajax({
        type:"GET",
        url:"/answer-vote-ajax/" + answer_id,
        dataType: "json",
        data: {"vote_type": vote_type},
        success: function (response) {
            vote_text.innerText = response.vote_count;
        },
        error: function () {
          alert("Hata oluştu !");
        },
    });
}



function commentDelete(itemType, commentId, commentType) {
    $.ajax({
        type: 'GET',
        url: '/delete-item/' + itemType + '/' + commentId,
        success: function (response) {
            if (response.message === 'success' && commentType === 'questionComment') {
                $('#queComment' + commentId).remove();
            } if (response.message === 'success' && commentType === 'answerComment') {
                $('#answerCommentField' + commentId).remove()
            }
        },
    })

}



function commentAdd(id, commentType) {
    let commentField, cmnt, form
    if (commentType === 'answerComment') {
        form = document.getElementById('answerCommentForm' + id)
    } else {
        commentField = document.getElementById('cmnt_field');
        cmnt = document.getElementById('commentsDiv');
        form = document.getElementById('questionCommentForm');
    }

    const formData = new FormData(form);
    formData.append("comment_type", commentType)

    $.ajax({
        type: 'POST',
        url: '/comment-add/' + id,
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            if (response.status === 'success' && commentType === 'questionComment') {
                const newCommentHTML = `
                        <div id="queComment${response.commentId}" style="width: 50rem; position: relative; top: 32rem; left: 12rem; border-top: 1px solid rgb(190, 190, 190); word-wrap: break-word; padding: 5px 20px 5px 20px; cursor: pointer;">
                            <p>${response.comment} - ${response.commentUser} &nbsp; <em style="opacity: 0.5;">${response.commentDate}</em>
                            <a onclick="commentDelete('question_comment', ${response.commentId}, 'questionComment')" class="stil" style="float: right;">Sil</a>
                            </p>
                        </div>
                    `;

                $('#comments').prepend(newCommentHTML);
                commentField.style.opacity = "0";
                cmnt.style.marginTop = "0";
                form.reset();

            } if (response.status === 'success' && commentType === 'answerComment') {

                const newAnsCommentHTML = `
                    <div id="answerCommentField${response.commentId}" style="border-top: 1px solid #ccc; margin: 60px 0 -60px 50px; padding: 5px 20px 5px 20px; word-wrap: break-word; width: 50rem;">
                        <p>${response.comment} - ${response.commentUser} &nbsp; <em style="opacity: 0.5;">${response.commentDate}</em>
                        <a onclick="commentDelete('answer_comment', '${response.commentId}', 'answerComment')" class="stil" style="float: right;">Sil</a></p>
                    </div>`;

                $('#answer_comment_field' + id).prepend(newAnsCommentHTML);
                form.reset();
                form.style.display = "none"
            }
        }
    })
}

