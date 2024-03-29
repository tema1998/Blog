const followBtn = document.querySelector('.btn-follow');
const followerBox = document.querySelector('.followers-box');

//followBtn.addEventListener('click', function() {
//    console.log('123')
//})

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

if (followBtn){
    followBtn.addEventListener('click', event => {
    const userId = event.target.dataset.userid
    fetch(`/user/follow/${userId}/`, {
        method: 'POST',
        headers: {
            "X-CSRFToken": csrftoken,
            "X-Requested-With": "XMLHttpRequest",
    }}).then(response => response.json())
    .then(data => {
        const isBtnPrimary = followBtn.classList.contains('btn-primary');
        const message = data.message || '';

        if (isBtnPrimary) {
            followBtn.classList.remove('btn-primary');
            followBtn.classList.add('btn-danger');
        } else {
            followBtn.classList.remove('btn-danger');
            followBtn.classList.add('btn-primary');
        }
        followBtn.innerHTML = message;
        elementUpdate('.update-follower-data');
        });
    });
};
