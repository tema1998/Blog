const chatSocket = new WebSocket(
'ws://'
+ window.location.host
+'/ws/'
+ chatId
+'/'
);

chatSocket.onmessage = function(e) {

    const data = JSON.parse(e.data);

        if (data.message) {
        let html = '<div class="bg-white shadow rounded-md  -mx-2 lg:mx-0 py-2 px-2 mb-2 flex svg-messages-show"><div><a href="/profile/'
            html += data.username + '"> <img src="' + data.user_profile_img_url + '" class="bg-gray-200 border border-white rounded-full w-8 h-8"> </a>'
            html += '</div><div class="pl-2 basis-full"><div class="font-semibold flex justify-between "><div class="basis-2/4"><a href="/profile/'
            html += data.username + '">' + data.username + '</a></div><div>' + data.date_added + '</div><div class="svg-messages-hide"><form action="'
            html += delete_message_url + '" method="POST">' + '<input type="hidden" name="csrfmiddlewaretoken" value="' + csrf_token + '">'
            html += '<input type="hidden" value="' + data.message_id
            html += '" name="message_id"><button><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">'
            html += '<path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />'
            html += '</svg></button></form></div></div><div>' + data.message + '</div></div></div>'

        document.querySelector('#chat-messages').innerHTML += html;

        scrollToBottom();

    } else {
        alert('The message was empty!');
}}

chatSocket.onclose = function(e) {
    console.log('onclose')
}

document.querySelector('#chat-message-submit').onclick = function (e) {
    e.preventDefault();

    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;

    chatSocket.send(JSON.stringify({
        'message': message,
        'username': userName,
        'chat': chatId,
    }));

    messageInputDom.value = '';

    return false;
    }

    function scrollToBottom() {
        const objDiv = document.querySelector('#chat-messages');
        objDiv.scrollTop = objDiv.scrollHeight;
    }

    scrollToBottom();