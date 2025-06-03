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
        headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
        body: JSON.stringify({ class_id: classId })
    });
    const data = await resp.json();
    const studentList = document.getElementById('studentList');
    studentList.innerHTML = "";
    data.students.forEach(student => {
        const li = document.createElement("li");
        li.textContent = student.username;
        studentList.appendChild(li);
    });
}