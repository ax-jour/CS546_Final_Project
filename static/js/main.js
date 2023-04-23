
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
    const challengeForm = document.querySelector("#challenge");
    const createAccountForm = document.querySelector("#createAccount");
    const linkCreateAccount = document.querySelector("#linkCreateAccount");
    const linkLogin = document.querySelector("#linkLogin");
    const voteResult = document.querySelector("#voteResult");
    const voting = document.querySelector("#voting");

    if (linkCreateAccount || linkLogin) {
        /**
         * Switch from login page to signup page
         */
        linkCreateAccount.addEventListener("click", e => {
            e.preventDefault();
            loginForm.classList.add("form--hidden");
            createAccountForm.classList.remove("form--hidden");
        });

        /**
         * Switch from signup page to login page
         */
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
            const driver_license = thirdpartyForm.querySelector("#license").value;
            fetch('http://localhost:5000/get_invitation_code', {
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
            const invitation_code = loginForm.querySelector("#login_invitation").value;
            fetch('http://localhost:5000/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ invitation_code })
            })
                .then(response => {
                    if (response.ok) { return response.json() }
                    return Promise.reject(response);
                })
                .then(responseJson => {
                    window.location.replace("http://localhost:5000/challenge_page");
                })
                .catch(err => {
                    err.json()
                        .then(data => { setFormMessage(loginForm, "error", data.message) });
                });
        });
    }


    if (createAccountForm) {
        createAccountForm.addEventListener("submit", e => {
            e.preventDefault();
            const first_name = createAccountForm.querySelector("#first").value;
            const last_name = createAccountForm.querySelector("#last").value;
            const invitation = createAccountForm.querySelector("#signup_invitation").value;
            fetch('http://localhost:5000/signup', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ first_name, last_name, invitation })
            })
                .then(response => {
                    if (response.ok) { return response.json() }
                    return Promise.reject(response);
                })
                .then(responseJson => {
                    window.location.replace("http://localhost:5000/challenge_page");
                })
                .catch(err => {
                    err.json()
                        .then(data => { setFormMessage(createAccountForm, "error", data.message) });
                });
        });
    }


    if (challengeForm) {
        challengeForm.addEventListener("submit", e => {
            e.preventDefault();
            const first_name = challengeForm.querySelector("#first").value;
            const last_name = challengeForm.querySelector("#last").value;

            fetch('http://localhost:5000/challenge', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ first_name, last_name })
            })
                .then(response => {
                    if (response.ok) { return response.json() }
                    return Promise.reject(response);
                })
                .then(responseJson => {
                    setFormMessage(challengeForm, "success", responseJson.message);
                    window.location.replace("http://localhost:5000/vote_page");
                })
                .catch(err => {
                    err.json()
                        .then(err => {
                            setFormMessage(challengeForm, "error", err.message)
                        });
                    // .then(() => { 
                    //     fetch('http://localhost:5000/logout', {
                    //         method: 'POST',
                    //         headers: { 'Content-Type': 'application/json' },
                    //     }).then((response) => {
                    //         if (response.ok) { return response.json() }
                    //         return Promise.reject(response);
                    //     })
                    //     .then(() => {
                    //         window.location.replace("http://localhost:5000/");
                    //     })
                    //     .catch(err => {
                    //         err.json()
                    //         .then(data => { setFormMessage(challengeForm, "error", data.message) });
                    //     });
                    // });
                });

        });

        challengeForm.querySelector("#logout").addEventListener("click", e => {
            e.preventDefault();
            fetch('http://localhost:5000/logout', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
            }).then((response) => {
                if (response.ok) { return response.json() }
                return Promise.reject(response);
            })
                .then(() => {
                    window.location.replace("http://localhost:5000/");
                })
                .catch(err => {
                    err.json()
                        .then(data => { setFormMessage(challengeForm, "error", data.message) });
                });
        });
    }


    if (voting) {        
        voting.querySelectorAll('.btn').forEach(btn => {
            btn.addEventListener("click", e => {
                e.preventDefault();
                let candidate = btn.getAttribute("id");
                fetch('http://localhost:5000/vote', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ candidate })
                })
                .then(response => {
                    if (response.ok) { return response.json() }
                    return Promise.reject(response);
                })
                .then(responseJson => {
                    window.location.replace("http://localhost:5000/vote_result");
                })
                .catch(err => {
                    err.json()
                    .then(data => { setFormMessage(voting, "error", data.message) });
                });
            });
        });

        document.querySelector("#logout").addEventListener("click", e => {
            e.preventDefault();
            fetch('http://localhost:5000/logout', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
            }).then((response) => {
                if (response.ok) { return response.json() }
                return Promise.reject(response);
            })
            .then(() => { 
                window.location.replace("http://localhost:5000/"); 
            })
            .catch(err => {
                err.json()
                .then(data => { setFormMessage(voting, "error", data.message) });
            });
        });
    }


if (voteResult) {
    console.log("voteResult");

    document.querySelector("#logout").addEventListener("click", e => {
        e.preventDefault();
        fetch('http://localhost:5000/logout', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
        }).then((response) => {
            if (response.ok) { return response.json() }
            return Promise.reject(response);
        })
            .then(() => {
                window.location.replace("http://localhost:5000/");
            })
            .catch(err => {
                err.json()
                    .then(data => { setFormMessage(voting, "error", data.message) });
            });
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