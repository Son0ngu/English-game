const form = document.querySelector('.profile-form');
const avatarInput = document.getElementById('avatar');
const avatarPreview = document.getElementById('avatarPreview');
const listContainer = document.getElementById("classList");

const fields = [
    { input: 'profileUsername', type: 'text', min: 4 },
    { input: 'profileEmail', type: 'email' },
];
const pwdFields = [
    { input: 'currentPassword', type: 'password', min: 8 },
    { input: 'newPassword', type: 'password', min: 8 },
    { input: 'confirmPassword', type: 'password', min: 8 },
];

// avatarInput.addEventListener('change', () => {
//     const file = avatarInput.files[0];
//     if (!file) return;
//     if (!file.type.startsWith('image/')) {
//         showError('avatarError', 'Chỉ chấp nhận ảnh.');
//         return;
//     }
//     clearError('avatarError');
//     const reader = new FileReader();
//     reader.onload = e => avatarPreview.src = e.target.result;
//     reader.readAsDataURL(file);
// });

function showError(idOrSpan, msg) {
    let span = (typeof idOrSpan === 'string')
        ? document.getElementById(idOrSpan)
        : idOrSpan;
    span.textContent = msg;
}

function clearError(idOrSpan) {
    let span = (typeof idOrSpan === 'string')
        ? document.getElementById(idOrSpan)
        : idOrSpan;
    span.textContent = '';
}

async function onProfileSubmit(e) {
    e.preventDefault();
    let valid = true;

    // Xóa lỗi cũ
    document.querySelectorAll('.field .error').forEach(s => s.textContent = '');

    // validate avatar (nếu muốn bắt buộc thì kiểm thêm .files.length)

    // validate username & email
    for (let f of fields) {
        const inp = document.getElementById(f.input);
        const err = inp.nextElementSibling;
        if (!inp.checkValidity() ||
            (f.min && inp.value.length < f.min)) {
            err.textContent = `Không hợp lệ.`;
            inp.focus();
            valid = false;
        }
    }

    // nếu user mở phần đổi mật khẩu thì validate password
    if (document.querySelector('.change-password').open) {
        for (let f of pwdFields) {
            const inp = document.getElementById(f.input);
            const err = inp.nextElementSibling;
            if (!inp.checkValidity() ||
                (f.min && inp.value.length < f.min)) {
                err.textContent = `Không hợp lệ.`;
                inp.focus();
                valid = false;
            }
        }
        // kiểm new vs confirm match
        const np = document.getElementById('newPassword'),
            cp = document.getElementById('confirmPassword');
        if (np.value !== cp.value) {
            showError(cp.nextElementSibling, 'Mật khẩu không khớp.');
            valid = false;
        }
    }

    if (!valid) return;

    // giả lập loading
    const btn = form.querySelector('button');
    const loadingMsg = document.getElementById('loadingMsg');
    btn.textContent = 'Đang lưu...';
    loadingMsg.textContent = 'Vui lòng chờ...';
    await new Promise(r => setTimeout(r, 1500));
    loadingMsg.textContent = '';
    btn.textContent = 'Lưu thay đổi';

    // tại đây bạn có thể gọi API lên server...
}

document.addEventListener("DOMContentLoaded", () => {
    const logoutBtn = document.getElementById("logoutBtn");
    if (logoutBtn) {
        console.log("dang bam logout")
        logoutBtn.addEventListener("click", () => {
            console.log("dang bam logout")
            localStorage.removeItem("token");
            alert("Bạn đã đăng xuất.");

            // Hiện lại tab login
            const loginTabItem = document.querySelector('a[href="#login"]')?.closest("li");
            const userTabItem = document.querySelector('#nav-user');
            const loginTabLink = document.querySelector('a[href="#login"]');

            if (loginTabItem) loginTabItem.style.display = "block";
            if (userTabItem) userTabItem.style.display = "none";

            if (loginTabLink) loginTabLink.click();

            window.location.reload();
        });
    }
});

document.addEventListener("DOMContentLoaded", () => {
    loadClasses(); // hoặc tuỳ vào hàm loadClasses() bạn đang dùng
    console.log("dang goi ham loadclasses")

    // 2. Gán event cho nút Tạo lớp
    const createClassBtn = document.getElementById("createClassBtn");
    if (createClassBtn) {
        createClassBtn.addEventListener("click", async () => {
            const nameInput = document.getElementById("newClassName");
            const className = nameInput.value.trim();
            if (!className) {
                alert("Vui lòng nhập tên lớp.");
                return;
            }

            // Lấy token từ localStorage
            const token = localStorage.getItem("token");
            if (!token) {
                alert("Bạn cần đăng nhập trước.");
                return;
            }

            // Giải mã JWT để lấy teacher_id (giả sử identity được lưu thành sub)
            let teacherId = null;
            try {
                const payload = JSON.parse(atob(token.split('.')[1]));
                teacherId = payload.sub;  // sub = identity (username/teacher_id)
            } catch (err) {
                console.error("Invalid token format:", err);
                alert("Token không hợp lệ. Vui lòng đăng nhập lại.");
                return;
            }

            console.log(teacherId)

            // Gọi API create_class (giữ nguyên backend)
            try {
                const resp = await fetch("http://localhost:5000/classroom/create", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        name: className
                    })
                });

                const data = await resp.json();
                if (resp.ok) {
                    // Tạo thành công
                    nameInput.value = "";
                    // Reload lại danh sách lớp
                    loadClasses(); // hoặc tuỳ vào hàm loadClasses() bạn đang dùng
                    console.log("dang goi ham loadclasses")
                } else {
                    // Nếu backend trả về lỗi, hiển thị message
                    alert(data.error || "Không thể tạo lớp.");
                }
            } catch (err) {
                console.error("create class error:", err);
                alert("Lỗi khi kết nối server.");
            }
        });
    }
});



// Hàm load danh sách lớp của teacher
async function loadClasses() {
    const token = localStorage.getItem("token");
    if (!token) {
        alert("Bạn cần đăng nhập trước.");
        return;
    }
    try {
        const resp = await fetch("http://localhost:5000/classroom/classes", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({})
        });

        if (resp.ok) {
            const classesArray = await resp.json();
            listContainer.innerHTML = "";

            if (!Array.isArray(classesArray) || classesArray.length === 0) {
                listContainer.innerHTML = "<li>Chưa có lớp nào.</li>";
                return;
            }

            classesArray.forEach(cls => {
                const li = document.createElement("li");
                li.innerHTML = `
                    <span class="name">${cls.name}</span>
                    <span class="code">${cls.code}</span>
                `;

                // Thêm sự kiện click để chuyển hướng đến trang chi tiết lớp
                li.addEventListener('click', () => {
                    showClassDetails(cls.id, cls.name);
                });

                listContainer.appendChild(li);
            });

        } else {
            const text = await resp.text();
            console.error("Server returned non-OK status:", resp.status, text);
        }
    } catch (err) {
        console.error("load classes error:", err);
        alert("Lỗi khi kết nối server.");
    }
}

