const messages_container = document.getElementById('chat-messages')
var page = 1;
var empty_page = false;
var block_request = false;


function loadMessages() {
    block_request = true;
        page += 1;
        $.get('?page=' + page, function (data) {
            if (data === '') {
                empty_page = true;
            } else {
                block_request = false;
                last_element = document.getElementById('chat-messages').children[0]
                $('#chat-messages').prepend(data);
                messages_container.scrollTop = last_element.offsetTop;
                setTimeout(function() {}, 1000);
            }
        });
}
messages_container.onscroll = function () {
    if (messages_container.scrollTop == 0) {
        loadMessages();
    }
};

