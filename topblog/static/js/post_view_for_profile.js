let popupBgs = document.querySelectorAll('.popup__bg'); // Фон попап окна
let openPopupButtons = document.querySelectorAll('.open-popup'); // Кнопки для показа окна
let closePopupButtons = document.querySelectorAll('.close-popup'); // Кнопка для скрытия окна
let popupWindows = document.querySelectorAll('.popup');

//popupWindows.forEach((window) => {
//    window.addEventListener('wheel', function(e) {
//    e.stopPropagation();
//    e.preventDefault();
//    });
//});

openPopupButtons.forEach((button) => { // Перебираем все кнопки
    button.addEventListener('click', (e) => { // Для каждой вешаем обработчик событий на клик
        var postId = button.id
        e.preventDefault(); // Предотвращаем дефолтное поведение браузера
        //popupBg.classList.add('active'); // Добавляем класс 'active' для фона
        //popup.classList.add('active'); // И для самого окна
        let openPopupElements = document.querySelectorAll(`.a${postId}`);
        openPopupElements.forEach((element) => {
            element.classList.add('active');
        });
    });
});

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