document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");

    const showLoginLink = document.getElementById("showLogin");
    const showRegisterLink = document.getElementById("showRegister");
    const loginDiv = document.querySelector(".login-form");
    const registerDiv = document.querySelector(".register-form");

    form.addEventListener("submit", handleRegister);

    // Gắn sự kiện form
    if (loginForm) loginForm.addEventListener("submit", handleLogin);
    if (registerForm) registerForm.addEventListener("submit", handleRegister);

    // Toggle login/register
    if (showRegisterLink)
        showRegisterLink.addEventListener("click", (e) => {
            e.preventDefault();
            loginDiv.style.display = "none";
            registerDiv.style.display = "block";
        });

    if (showLoginLink)
        showLoginLink.addEventListener("click", (e) => {
            e.preventDefault();
            loginDiv.style.display = "block";
            registerDiv.style.display = "none";
        });

    // Nếu đã login trước đó thì hiển thị username
    const token = localStorage.getItem("token");
    if (token) {
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            const username = payload.sub;
            const loginTabItem = document.querySelector('a[href="#login"]')?.closest("li");
            const userTabLink = document.querySelector('a[href="#userprofile"]');
            const userTabItem = document.querySelector('#nav-user');

            if (loginTabItem) loginTabItem.style.display = "none";
            if (userTabLink && userTabItem) {
                userTabLink.textContent = payload.sub;
                userTabItem.style.display = "block";
                const activeTab = document.querySelector('.nav-link.active');
                if (activeTab && activeTab.getAttribute("href") === "#login") {
                    userTabLink.click();
                }
            }


            // Ẩn login/register nếu đã login
            if (loginDiv) loginDiv.style.display = "none";
            if (registerDiv) registerDiv.style.display = "none";
        } catch (err) {
            console.warn("Invalid token format", err);
        }
    }
});

async function handleLogin(event) {
    event.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    console.log("Logging in with:", { username, password });

    if (!username || !password) {
        alert("Please fill in all fields");
        return;
    }

    try {
        const response = await fetch("http://localhost:5000/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        const result = await response.json();
        console.log("Login response:", result);

        if (response.ok) {
            alert("Login successful!");
            localStorage.setItem("token", result.access_token);

            // Decode username từ token
            const payload = JSON.parse(atob(result.access_token.split('.')[1]));
            const loginTab = document.querySelector('a[href="#login"]');
            if (loginTab) loginTab.textContent = payload.sub;

            // Ẩn form
            document.querySelector(".login-form").style.display = "none";
            document.querySelector(".register-form").style.display = "none";

            window.location.reload();
        } else {
            alert(result.error || "Login failed.");
        }
    } catch (err) {
        console.error("Login error:", err);
        alert("Something went wrong.");
    }
}

async function handleRegister(event) {
    event.preventDefault();

    const username = document.getElementById("registerUsername").value.trim();
    const password = document.getElementById("registerPassword").value.trim();
    const confirm = document.getElementById("registerPasswordConfirm").value.trim();

    console.log("Registering with:", { username, password, confirm });

    if (!username || !password || !confirm) {
        alert("Please fill in all fields");
        return;
    }

    if (password !== confirm) {
        alert("Passwords do not match");
        return;
    }

    try {
        const response = await fetch("http://localhost:5000/auth/signup", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        const result = await response.json();
        console.log("Register response:", result);

        if (response.ok) {
            alert("Registration successful!");
            document.querySelector(".login-form").style.display = "block";
            document.querySelector(".register-form").style.display = "none";

            window.location.reload();
        } else {
            alert(result.error || "Registration failed.");
        }
    } catch (err) {
        console.error("Register error:", err);
        alert("Something went wrong.");
    }
}