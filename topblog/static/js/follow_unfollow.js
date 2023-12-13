const allFollowButtons = document.querySelector('#all-foollow-buttons');

allFollowButtons.addEventListener('click', event => {
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
//        const isBtnPrimary = followUnfollowBtn.classList.contains('btn-primary');
        const message = data.message || '';

//        if (isBtnPrimary) {
//            followUnfollowBtn.classList.remove('btn-primary');
//            followUnfollowBtn.classList.add('btn-danger');
//        } else {
//            followUnfollowBtn.classList.remove('btn-danger');
//            followUnfollowBtn.classList.add('btn-primary');
//        }
        target.innerHTML = message;
        });
});