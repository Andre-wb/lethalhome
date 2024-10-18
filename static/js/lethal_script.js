document.addEventListener('DOMContentLoaded', (event) => {
    const openButton = document.getElementById('open_button');
    const removeButton = document.getElementById('remove_button');
    const body = document.getElementById('body');
    const links = document.querySelector('.links');

    if (openButton) {
        openButton.addEventListener('click', (event) => {
            if (links) {
                links.classList.add('visible');
                openButton.classList.add('invisible');
                removeButton.classList.add('visible');
                body.classList.add('active');
            }
        });
    }

    if (removeButton) {
        removeButton.addEventListener('click', (event) => {
            if (links) {
                links.classList.remove('visible');
                openButton.classList.remove('invisible');
                removeButton.classList.remove('visible');
                body.classList.remove('active');
            }
        });
    }
});


