
function scrollComments() {
    var all_comments_lists = document.querySelectorAll('#comments_list');
    for (var i = 0; i < all_comments_lists.length; ++i) {
        all_comments_lists[i].scrollTo({
              top: all_comments_lists[i].scrollHeight,
              behavior: 'smooth'
        });
    };
};

scrollComments();