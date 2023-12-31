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



function questionCommentAdd(question_id) {
    const commentField = document.getElementById('cmnt_field');
    const cmnt = document.getElementById('comments');
    const form = document.getElementById('commentForm');
    const commentInput = document.getElementById('queCommentId').value;

    const formData = new FormData(form);
    formData.append('question_id', question_id);
    formData.append('comment', commentInput);

    $.ajax({
        type: 'POST',
        url: '/ques-comment-form/' + question_id,
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            if (response.message === 'success') {
                const newCommentHTML = `
                        <div id="queComment${response.commentId}" style="width: 50rem; position: relative; top: 32rem; left: 12rem; border-top: 1px solid rgb(190, 190, 190); word-wrap: break-word; padding: 5px 20px 5px 20px; cursor: pointer;">
                            <p>${commentInput} - ${response.commentUser} &nbsp; <em style="opacity: 0.5;">${response.published_date}</em>
                            <a onclick="deleteComment('question_comment', ${response.commentId})" class="stil" style="float: right;">Sil</a>
                            </p>
                        </div>
                    `;
            $('#comments').prepend(newCommentHTML);
        
                commentField.style.opacity = "0";
                cmnt.style.marginTop = "0";
                form.reset();

            };
        },
        error: function () {
            alert('Hata oluştu!');
        },
    });
}





function deleteComment(itemType, commentId) {
    $.ajax({
        type: 'GET',
        url: '/delete-item/' + itemType + '/' + commentId,
        success: function(response) {
            if (response.message === 'success') {
               $('#queComment' + commentId).remove();
            }
        },
        error: function() {
            alert('hata oluştu.');
        }
    });
}





function answerCommentAdd(answer_id) {
    const ansCmntField = document.getElementById('ans_cmnt_field') 
    const ansCmntForm = document.getElementById('ans_comment_form' + answer_id)

    const formData = new FormData(ansCmntForm)
    formData.append('answer_id', answer_id)
    formData.append('ansComment', ansCmntField)


    $.ajax({
        type: 'POST',
        url: '/comment/' + answer_id,
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            if (response.message === 'success') {
                const newAnsCommentHTML = `
                    <div id="ansCommentField${response.commentId}" style="border-top: 1px solid #ccc; margin: 60px 0px -60px 50px; padding: 5px 20px 5px 20px; word-wrap: break-word; width: 50rem;">
                        <p>${response.formValue} - ${response.user} &nbsp; <em style="opacity: 0.5;">${response.PubDate}</em>
                        <a onclick="ansCommentDelete('answer_comment', '${response.commentId}')" class="stil" style="float: right;">Sil</a></p>
                    </div>`;
            
                $('#answer_comment_field' + answer_id).prepend(newAnsCommentHTML);
                ansCmntForm.reset();
            }
        }
    })
}



function ansCommentDelete(itemType, comment_id) {
    const ansComment = document.getElementById('ansCommentField' + comment_id)

    $.ajax({
        type: 'GET',
        url: '/delete-item/' + itemType + '/' + comment_id,
        success: function(response) {
            if (response.message === 'success') {
                ansComment.remove()
            }
        },
        error: function() {
            alert('Hata oluştu !')
        }
    })
}