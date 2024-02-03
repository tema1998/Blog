const profilesWrap = document.querySelector('#profiles-wrap');

profilesWrap.addEventListener('click', event => {
    let target = event.target;
    if (target.id != 'btn-follow-unfollow') return;

    const userId = event.target.dataset.userid
    fetch(`/user/follow/${userId}/`, {
        method: 'POST',
        headers: {
            "X-CSRFToken": csrftoken,
            "X-Requested-With": "XMLHttpRequest",
    }}).then(response => response.json())
    .then(data => {
        const message = data.message || '';
        target.innerHTML = message;
        });
});