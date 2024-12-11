document.addEventListener('DOMContentLoaded', (event) => {
    const body = document.getElementById('body');
    const links = document.querySelector('.links');
    const button = document.getElementById('menu');
    const footer = document.getElementById('footer');

    if (button) {
        button.addEventListener('click', () => {
            if (button.classList.contains('active')) {
                button.classList.remove('active');
                links.classList.remove('visible');
                body.classList.remove('active');
                footer.classList.remove('active');
            } else {
                button.classList.add('active');
                links.classList.add('visible');
                body.classList.add('active');
                footer.classList.add('active');
            }
        });
    }
});



