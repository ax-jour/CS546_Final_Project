
/**
 * Setting messages and inputs errors
 */
function setFormMessage(formElement, type, message) {
    const messageElement = formElement.querySelector(".form__message");

    messageElement.textContent = message;
    messageElement.classList.remove("form__message--success", "form__message--error");
    messageElement.classList.add(`form__message--${type}`);
}

function setInputError(inputElement, message) {
    inputElement.classList.add("form__input--error");
    inputElement.parentElement.querySelector(".form__input-error-message").textContent = message;
}

function clearInputError(inputElement) {
    inputElement.classList.remove("form__input--error");
    inputElement.parentElement.querySelector(".form__input-error-message").textContent = "";
}


/**
 * Add event listeners after DOM has loaded
 */
document.addEventListener("DOMContentLoaded", () => {
    const thirdpartyForm = document.querySelector("#thirdparty");
    const loginForm = document.querySelector("#login");
    const createAccountForm = document.querySelector("#createAccount");
    const linkCreateAccount = document.querySelector("#linkCreateAccount");
    const linkLogin = document.querySelector("#linkLogin");

    /**
     * Switch from login page to signup page
     */
    if (linkCreateAccount) {
        linkCreateAccount.addEventListener("click", e => {
            e.preventDefault();
            loginForm.classList.add("form--hidden");
            createAccountForm.classList.remove("form--hidden");
        });
    }

    /**
     * Switch from signup page to login page
     */
    if (linkLogin) {
        linkLogin.addEventListener("click", e => {
            e.preventDefault();
            loginForm.classList.remove("form--hidden");
            createAccountForm.classList.add("form--hidden");
        });
    }

    /**
     * Third party form submission
     */
    if (thirdpartyForm) {
        thirdpartyForm.addEventListener("submit", e => {
            e.preventDefault();
            const first_name = thirdpartyForm.querySelector("#first").value;
            const last_name = thirdpartyForm.querySelector("#last").value;
            const driver_license = thirdpartyForm.querySelector("#driver").value;
            fetch('http://localhost:5000/get_verification_code', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ first_name, last_name, driver_license })
            }).then(res => {
                if (res.ok) {
                    return res.json();
                }
                throw new Error('Something went wrong');
            }).then(data => {
                console.log(data);
                let str = "Your verification code is: " + data.message;
                setFormMessage(thirdpartyForm, "success", str);
            }).catch(err => {
                console.log(err);
            });
        });
    }
    


    /**
     * Login form submission
     */
    if (loginForm) {
        loginForm.addEventListener("submit", e => {
            e.preventDefault();
            // perform login

            setFormMessage(loginForm, "error", "Invalid username/password");
        });
    }

    document.querySelectorAll(".form__input").forEach(inputElement => {
        inputElement.addEventListener("blur", e => {
        });

        inputElement.addEventListener("input", e => {
            clearInputError(inputElement);
        });
    });
});