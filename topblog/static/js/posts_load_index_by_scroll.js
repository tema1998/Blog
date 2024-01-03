var page = 1;
var empty_page = false;
var block_request = false;
$('#end_posts').hide();


function loadContent() {
    block_request = true;
        page += 1;
        $.get('?page=' + page, function (data) {
            if (data === '') {
                empty_page = true;
                $('#end_posts').show();
                $('#lazy_more').hide();
            } else {
                block_request = false;
                $('#post_list').append(data);
                scrollComments();
            }
        });
}

window.addEventListener('scroll', () => {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight-5) {
        loadContent();
}
});

