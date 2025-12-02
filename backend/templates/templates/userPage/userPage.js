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

// document.addEventListener("DOMContentLoaded", () => {
//     loadClasses(); // hoặc tuỳ vào hàm loadClasses() bạn đang dùng
//     console.log("dang goi ham loadclasses")


// });



document.addEventListener('DOMContentLoaded', async () => {
    // 1. Lấy user hiện tại
    const resp = await fetch('http://localhost:5000/auth/HuyTranLayRoleTuID', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${localStorage.getItem("token")}` },
        body: JSON.stringify({})
    });
    if (!resp.ok) return console.error('Không lấy được thông tin user');
    const user = await resp.json();
    const role = user.role; // "teacher" hoặc "student"

    console.log("role:", role);

    // 2. Hiển thị section tương ứng
    if (role === 'teacher') {
        document.getElementById('teacherSection').style.display = 'block';
        loadTeacherClasses();
    } else {
        document.getElementById('studentSection').style.display = 'block';
        loadStudentClasses();
    }

    // Hàm load danh sách lớp của teacher
    async function loadTeacherClasses() {
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
                    alert("Lớp đã được tạo thành công.");
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

    // 3 --- Event: Student join lớp ---
    const joinClassBtn = document.getElementById("joinClassBtn");
    if (joinClassBtn) {
        joinClassBtn.addEventListener('click', async () => {
            console.log("dang bam join class")
            const code = document.getElementById('joinClassCode').value.trim();
            if (!code) return alert('Nhập mã lớp');
            console.log("code:", code);
            const r = await fetch('http://localhost:5000/classroom/join', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${localStorage.getItem("token")}` },
                body: JSON.stringify({ class_code: code })
            });
            if (r.ok) {
                document.getElementById('joinClassCode').value = '';
                loadStudentClasses();
            } else {
                const e = await r.json();
                alert(e.error || 'Tham gia thất bại');
            }
        });
    }

    // --- Hàm cho Student load danh sách lớp đã join ---
    async function loadStudentClasses() {
        const r = await fetch('http://localhost:5000/classroom/student/classes', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${localStorage.getItem("token")}` },
            body: JSON.stringify({})
        });
        const { classes } = await r.json();
        // classes là object { id1: {…}, id2: {…}, … }
        const ul = document.getElementById('joinedClassList');
        ul.innerHTML = '';
        Object.values(classes).forEach(c => {
            const li = document.createElement('li');
            li.className = 'list-group-item d-flex justify-content-between align-items-center';
            li.innerHTML = `
        <span>${c.name} (${c.code})</span>
        <button class="btn btn-sm btn-outline-secondary view-students" data-id="${c.id}">
          Xem SV
        </button>
      `;
            ul.appendChild(li);
        });
        document.querySelectorAll('#joinedClassList .view-students').forEach(btn =>
            btn.addEventListener('click', () => loadStudentsInClass(btn.dataset.id))
        );
    }

    // --- Hàm chung: load danh sách sinh viên trong 1 lớp ---
    async function loadStudentsInClass(classId) {
        const r = await fetch('http://localhost:5000/classroom/students', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${localStorage.getItem("token")}` },
            body: JSON.stringify({ class_id: classId })
        });
        if (!r.ok) {
            const e = await r.json();
            return alert(e.error || 'Không lấy được danh sách sinh viên');
        }
        const { students } = await r.json();
        // Hiển thị popup hoặc modal, ở đây tạm dùng alert
        const names = students.map(s => `${s.id} — ${s.email}`).join('\n');
        alert(`Sinh viên lớp ${classId}:\n` + names);
    }
});