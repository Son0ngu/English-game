const form = document.getElementsByTagName('form')[0];

const usernameLabel = document.querySelector('[for="username"]');
const usernameError = document.querySelector('[for="username"] + .error')
const usernameInput = document.getElementById('username');

const passwordLabel = document.querySelector('[for="password"]');
const passwordError = document.querySelector('[for="password"] + .error')
const passwordInput = document.getElementById('password');

const submitButton = document.querySelector('button[type="submit"]')

const ssrLoadingRead = document.getElementById('js-loadingMsg')



function timeout(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

let isSubmitting = false
async function onSubmit(event) {
    event.preventDefault()
    if (isSubmitting) return
    isSubmitting = true
    usernameLabel.parentElement.classList.remove('active-error')
    usernameError.textContent = ''
    passwordLabel.parentElement.classList.remove('active-error')
    passwordError.textContent = ''
    if (!passwordInput.validity.valid) {
        passwordLabel.parentElement.classList.add('active-error')
        passwordError.textContent = '- Invalid Password'
        passwordInput.focus()
    }
    if (!usernameInput.validity.valid) {
        usernameLabel.parentElement.classList.add('active-error')
        usernameError.textContent = '- Invalid Username'
        usernameInput.focus()
    }
    if (passwordInput.validity.valid && usernameInput.validity.valid) {
        submitButton.textContent = "Loading..."
        ssrLoadingRead.textContent = "Logging in. Please wait..."
        await timeout(2000)
        ssrLoadingRead.textContent = ""
        submitButton.textContent = "Login"
    }
    // probably have error messages for each `.validity.tooShort` etc...
    isSubmitting = false
}