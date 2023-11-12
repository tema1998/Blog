var page = 1;
var empty_page = false;
var block_request = false;
$('#end_posts').hide();

$('#lazy_more').click(function (e) {
    e.preventDefault();
    if (empty_page === false && block_request === false) {
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
            }
        });
    }
});