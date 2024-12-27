document.addEventListener('DOMContentLoaded', (event) => {
    const body = document.getElementById('body');
    const links = document.querySelector('.links');
    const button = document.getElementById('menu');
    const footer = document.getElementById('footer');
    const form = document.querySelector('form');
    const inputs = form ? form.querySelectorAll('input') : [];

    if (form) {
        form.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();

                const inputValues = Array.from(inputs).map(input => input.value.trim().toLowerCase());
                if (inputValues.includes('вход')) {
                    window.location.href = '/login';
                    return;
                }
                if (inputValues.includes('регистрация')) {
                    window.location.href = '/register';
                    return;
                }

                const allFieldsFilled = inputValues.every(value => value !== '');
                if (allFieldsFilled) {
                    form.submit();
                } else {
                    const emptyField = Array.from(inputs).find(input => input.value.trim() === '');
                    if (emptyField) emptyField.focus();
                }
            }
        });
    }


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

    // Для постоянного фокуса на log_index.html
    const logIndexInput = document.querySelector('#input');
    if (logIndexInput) {
        logIndexInput.focus();

        document.addEventListener('focusin', function (event) {
            if (event.target !== logIndexInput) {
                logIndexInput.focus();
            }
        });

        setInterval(function () {
            if (document.activeElement !== logIndexInput) {
                logIndexInput.focus();
            }
        }, 50);
    }

    window.onload = function () {
        const formElements = document.querySelectorAll('input[class]:not([class="hidden"])');
        const form = document.querySelector('form');

        if (formElements.length > 0) {
            let currentIndex = 0;
            const shownElements = new Set();

            function setFocus() {
                formElements[currentIndex].focus();
            }

            function isCurrentFieldEmpty() {
                return formElements[currentIndex].value.trim() === "";
            }

            function updateClasses() {
                formElements.forEach((element, index) => {
                    const label = document.querySelector(`label[for="${element.id}"]`);
                    if (index === currentIndex && !shownElements.has(index)) {
                        element.classList.remove('hidden');
                        shownElements.add(index);
                        if (label) label.classList.remove('hidden');
                    } else if (!shownElements.has(index)) {
                        element.classList.add('hidden');
                        if (label) label.classList.add('hidden');
                    }
                });
            }

            function handleFormSubmit() {
                if (form.id === "registerForm") {
                    const password = document.querySelector('input[name="password"]').value;
                    const confirmPassword = document.querySelector('input[name="confirm_password"]').value;

                    if (password && confirmPassword && password === confirmPassword) {
                        form.submit();
                    }
                } else if (form.id === "loginForm") {
                    form.submit();
                }
            }

            setFocus();
            updateClasses();

            document.addEventListener('focusin', function (event) {
                if (!Array.from(formElements).includes(event.target)) {
                    setFocus();
                }
            });

            document.addEventListener('keydown', function (e) {
                if (e.key === 'Enter') {
                    if (isCurrentFieldEmpty()) {
                        e.preventDefault();
                        return setFocus();
                    }

                    if (currentIndex === formElements.length - 1) {
                        e.preventDefault();
                        return handleFormSubmit();
                    }

                    currentIndex = (currentIndex + 1) % formElements.length;
                    setFocus();
                    updateClasses();
                    e.preventDefault();
                }
            });

            document.addEventListener('keydown', function (e) {
                if (e.key === 'Tab') {
                    if (isCurrentFieldEmpty()) {
                        e.preventDefault();
                        return setFocus();
                    }
                    currentIndex = (currentIndex - 1 + formElements.length) % formElements.length;
                    setFocus();
                    updateClasses();
                    e.preventDefault();
                }
            });

            setInterval(function () {
                if (document.activeElement !== formElements[currentIndex]) {
                    setFocus();
                }
            }, 50);
        }
    };
});
