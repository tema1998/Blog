const postWrap = document.querySelector('#post_list');
svg = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"> <path stroke-linecap="round" stroke-linejoin="round" d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z" /></svg>'
svg_fill = '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="fill-black w-6 h-6"> <path stroke-linecap="round" stroke-linejoin="round" d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z" /></svg>'

async function elementUpdate(selector) {
  try {
    var html = await (await fetch(location.href)).text();
    var newdoc = new DOMParser().parseFromString(html, 'text/html');
    document.querySelector(selector).outerHTML = newdoc.querySelector(selector).outerHTML;
    return true;
  } catch(err) {
    console.error(err);
    return false;
  }
}

postWrap.addEventListener('click', event => {
    let target = event.target;
    if (target.id == 'add-remove-favorite') {
    const postId = event.target.dataset.postid
    fetch(`/add-remove-favorites/${postId}/`, {
        method: 'POST',
        headers: {
            "X-CSRFToken": csrftoken,
            "X-Requested-With": "XMLHttpRequest",
    }}).then(response => response.json())
    .then(data => {
        if (data.post_status == true) {
            var message = svg_fill + data.message;
        }
        else {
            var message = svg + data.message;
        }
        target.innerHTML = message;
        });
        }
    else if (target.id == 'like-post-button') {
    const postId = event.target.dataset.postid
    fetch(`/like-post/${postId}/`, {
        method: 'POST',
        headers: {
            "X-CSRFToken": csrftoken,
            "X-Requested-With": "XMLHttpRequest",
    }}).then(response => response.json())
    .then(data => {
        likecounter = document.querySelector('[data-likecounter="'+postId+'"]');
        likesvg = document.querySelector('[data-likesvg="'+postId+'"]');
        likecounter.innerHTML = data.likes
        if (data.like_status == true) {
            likesvg.classList.add("fill-current");
        }
        else {
            likesvg.classList.remove("fill-current");
        };

        });
        }

    else if (target.id == 'like-comment-button') {
        const commentId = event.target.dataset.commentid
        fetch(`/like-comment/${commentId}/`, {
            method: 'POST',
            headers: {
                "X-CSRFToken": csrftoken,
                "X-Requested-With": "XMLHttpRequest",
        }}).then(response => response.json())
        .then(data => {
            comment_like_counter = document.querySelector('[data-commentlikecounter="'+commentId+'"]');
            commentlikesvg = document.querySelector('[data-likecommentsvg="'+commentId+'"]');
            comment_like_counter.innerHTML = data.likes
            if (data.like_status == true) {
                commentlikesvg.classList.add("fill-current");
            }
            else {
                commentlikesvg.classList.remove("fill-current");
            };
            });
        }
});