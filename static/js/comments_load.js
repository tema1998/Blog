const button_load_comments = document.getElementById('load_comments')

function loadComments() {
        $.get('load-comments', function (data) {
            $('#comments_list').append(data);
        });
}

button_load_comments.addEventListener('click', () => {
        loadComments();
});
