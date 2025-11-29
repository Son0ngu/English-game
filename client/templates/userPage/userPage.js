const form = document.querySelector('.profile-form');
const avatarInput = document.getElementById('avatar');
const avatarPreview = document.getElementById('avatarPreview');

const fields = [
    { input: 'profileUsername', type: 'text', min: 4 },
    { input: 'profileEmail', type: 'email' },
];
const pwdFields = [
    { input: 'currentPassword', type: 'password', min: 8 },
    { input: 'newPassword', type: 'password', min: 8 },
    { input: 'confirmPassword', type: 'password', min: 8 },
];

avatarInput.addEventListener('change', () => {
    const file = avatarInput.files[0];
    if (!file) return;
    if (!file.type.startsWith('image/')) {
        showError('avatarError', 'Chỉ chấp nhận ảnh.');
        return;
    }
    clearError('avatarError');
    const reader = new FileReader();
    reader.onload = e => avatarPreview.src = e.target.result;
    reader.readAsDataURL(file);
});

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
