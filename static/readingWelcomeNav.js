const menuBtn = document.getElementById('menuBtn');
const menu = document.querySelector('.menu');
const menuText = document.querySelectorAll('.menuText');
menuBtn.addEventListener('click', () => {
    menu.classList.toggle('open');
    menuText.forEach(function (text, index) {
        setTimeout(() => {
            text.classList.toggle('open2');
        }, index * 50);
    });
});