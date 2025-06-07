function showClassDetails(classId, className) {
    document.querySelector('.profile-form').style.display = 'none';
    document.getElementById('classDetails').style.display = 'block';
    document.getElementById('classDetailsName').textContent = className;

    loadDashboard(classId);
    loadStudentList(classId);
}

function backToProfile() {
    document.querySelector('.profile-form').style.display = 'block';
    document.getElementById('classDetails').style.display = 'none';
}

async function loadDashboard(classId) {
    const token = localStorage.getItem("token");
    const resp = await fetch("http://localhost:5000/classroom/dashboard", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ class_id: classId })
    });
    console.log(classId)
    const data = await resp.json();
    document.getElementById('dashboard').textContent = JSON.stringify(data.dashboard);
}

async function loadStudentList(classId) {
    const token = localStorage.getItem("token");
    const resp = await fetch("http://localhost:5000/classroom/students", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ class_id: classId })
    });

    const data = await resp.json();
    console.log("Danh sách học sinh:", data);

    // **Đảm bảo studentList được khai báo trước khi dùng**
    const studentList = document.getElementById('studentList');
    studentList.innerHTML = ""; // Xóa sạch <li> cũ trước khi thêm mới

    data.students.forEach(student => {
        // Lấy id và tên đăng nhập của từng học sinh
        console.log("ID của học sinh:", student.id);

        const li = document.createElement("div");
        // Tạo 2 <span> con để áp style .email và .sid
        const spanEmail = document.createElement("span");
        spanEmail.classList.add("email");
        spanEmail.textContent = student.email;

        const spanId = document.createElement("span");
        spanId.classList.add("sid");
        spanId.textContent = `ID: ${student.id}`;

        li.appendChild(spanEmail);
        li.appendChild(spanId);
        studentList.appendChild(li);

    });
}