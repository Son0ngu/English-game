async function showClassDetails(classId, className) {
    console.log("Showing class details for class ID:", classId);

    document.querySelector('.profile-form').style.display = 'none';
    document.getElementById('classDetails').style.display = 'block';
    document.getElementById('classDetailsName').textContent = className;

    // Lấy user hiện tại
    const resp = await fetch('http://localhost:5000/auth/HuyTranLayRoleTuID', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${localStorage.getItem("token")}` },
        body: JSON.stringify({})
    });
    if (!resp.ok) return console.error('Không lấy được thông tin user');
    const user = await resp.json();
    const role = user.role; // "teacher" hoặc "student"

    console.log("role:", role);

    // Lấy section thêm câu hỏi
    const addSec = document.getElementById('addQuestionSection');
    const addForm = document.getElementById('addQuestionForm');
    const resultDiv = document.getElementById('addQResult');

    // Gán classId vào input ẩn
    document.getElementById('addQClassId').value = classId;

    // Nếu là teacher, show section và gắn listener
    if (role === 'teacher') {
        addSec.style.display = 'block';

        addForm.addEventListener('submit', async e => {
            e.preventDefault();
            resultDiv.textContent = '';
            // Chuẩn bị payload
            const payload = {
                class_id: classId,
                text: document.getElementById('addQText').value.trim(),
                q_type: document.getElementById('addQType').value,
                difficulty: document.getElementById('addQDifficulty').value,
                choices: document.getElementById('addQChoices').value
                    .split(';').map(s => s.trim()).filter(s => s),
                correct_index: document.getElementById('addQCorrect').value.trim()
            };

            console.log("Submitting question:", payload);

            try {
                const res = await fetch('http://localhost:5000/classroom/add_question', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();

                if (res.ok && data.success) {
                    resultDiv.style.color = 'green';
                    resultDiv.textContent = 'Thêm câu hỏi thành công!';
                    addForm.reset();       // clear form
                } else {
                    resultDiv.style.color = 'red';
                    resultDiv.textContent = 'Lỗi: ' + (data.error || 'Không thêm được');
                }
            } catch (err) {
                console.error(err);
                resultDiv.style.color = 'red';
                resultDiv.textContent = 'Lỗi kết nối server';
            }
        });

    } else {
        // nếu không phải teacher thì ẩn
        addSec.style.display = 'none';
    }

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
    const { dashboard } = await resp.json();  // giả sử API trả về { dashboard: [...] } hoặc { dashboard: {...} }

    const tbl = document.getElementById('dashboard');
    tbl.innerHTML = '';  // clear cũ
    // Nếu dashboard là mảng các record
    if (Array.isArray(dashboard) && dashboard.length) {
        const fields = Object.keys(dashboard[0]);
        // Tạo THEAD
        const thead = document.createElement('thead');
        const headRow = document.createElement('tr');
        for (let f of fields) {
            const th = document.createElement('th');
            th.textContent = f;
            headRow.appendChild(th);
        }
        thead.appendChild(headRow);
        tbl.appendChild(thead);

        // Tạo TBODY
        const tbody = document.createElement('tbody');
        for (let item of dashboard) {
            const tr = document.createElement('tr');
            for (let f of fields) {
                const td = document.createElement('td');
                let v = item[f];
                if (Array.isArray(v)) v = v.join(', ');
                td.textContent = v;
                tr.appendChild(td);
            }
            tbody.appendChild(tr);
        }
        tbl.appendChild(tbody);

    } else if (dashboard && typeof dashboard === 'object') {
        // Nếu dashboard là object key->value, hiển thị 2 cột
        const thead = document.createElement('thead');
        const headRow = document.createElement('tr');
        headRow.innerHTML = `<th>Metric</th><th>Value</th>`;
        thead.appendChild(headRow);
        tbl.appendChild(thead);

        const tbody = document.createElement('tbody');
        for (let [k, v] of Object.entries(dashboard)) {
            const tr = document.createElement('tr');
            const tdKey = document.createElement('td');
            tdKey.textContent = k;
            const tdVal = document.createElement('td');
            tdVal.textContent = Array.isArray(v) ? v.join(', ') : v;
            tr.append(tdKey, tdVal);
            tbody.appendChild(tr);
        }
        tbl.appendChild(tbody);

    } else {
        // fallback nếu không có dữ liệu
        tbl.textContent = 'Không có dữ liệu dashboard.';
    }
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