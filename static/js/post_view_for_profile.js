var popupBgs = document.querySelectorAll('.popup__bg'); // Фон попап окна
var openPopupButtons = document.querySelectorAll('.open-popup'); // Кнопки для показа окна
var closePopupButtons = document.querySelectorAll('.close-popup'); // Кнопка для скрытия окна
var popupWindows = document.querySelectorAll('.popup');

var postList = document.querySelector('#post_list');

//popupWindows.forEach((window) => {
//    window.addEventListener('wheel', function(e) {
//    e.stopPropagation();
//    e.preventDefault();
//    });
//});

postList.addEventListener('click', event => {
    let target = event.target;
    if (target.id == 'small-post-image') {
        event.preventDefault();
        const postId = event.target.dataset.poppostid
        let openPopupElements = document.querySelectorAll('[data-popup="'+postId+'"]');
        openPopupElements.forEach((element) => {
            element.classList.add('active');
        });
    }
});



//openPopupButtons.forEach((button) => { // Перебираем все кнопки
//    button.addEventListener('click', (e) => { // Для каждой вешаем обработчик событий на клик
//        var postId = button.id
//        e.preventDefault(); // Предотвращаем дефолтное поведение браузера
//        let openPopupElements = document.querySelectorAll('[data-popup="'+postId+'"]');
//        openPopupElements.forEach((element) => {
//            element.classList.add('active');
//        });
//    });
//});

closePopupButtons.forEach((button) => { // Перебираем все кнопки
    button.addEventListener('click', (e) => {
        e.preventDefault(); // Предотвращаем дефолтное поведение браузера
        let elementsWithActive = document.querySelectorAll('.active');
        elementsWithActive.forEach((element) => {
            element.classList.remove('active');
        });
    });
});

//popupBgs.forEach((background) => { // Перебираем все фоны
//    background.addEventListener('click', (e) => {
//        e.preventDefault(); // Предотвращаем дефолтное поведение браузера
//        let elementsWithActive = document.querySelectorAll('.active');
//        elementsWithActive.forEach((element) => {
//            element.classList.remove('active');
//        });
//    });
//});



document.addEventListener('click', (e) => {
    if(e.target.classList.contains('popup__bg')) {
        let elementsWithActive = document.querySelectorAll('.active');
        elementsWithActive.forEach((element) => {
            element.classList.remove('active');
        });
    };
});