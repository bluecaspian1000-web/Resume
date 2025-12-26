const loginBtn = document.getElementById('loginBtn');
const errorMsg = document.getElementById('errorMsg');


loginBtn.addEventListener('click', async () => {
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();

    if (!username || !password) {
        errorMsg.textContent = "لطفاً همه فیلدها را پر کنید";
        errorMsg.style.display = 'block';
        return;
    }

    try {
        // گرفتن توکن
        const res = await fetch(`${API}/api/token/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await res.json();

        if (!res.ok) {
            errorMsg.textContent = data.detail || 'نام کاربری یا رمز عبور اشتباه است';
            errorMsg.style.display = 'block';
            return;
        }

        // ذخیره توکن در localStorage
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);

        // گرفتن اطلاعات کاربر (شامل نقش)
        const userRes = await fetch(`${API}/users/me/`, {
            headers: {  
                      'Authorization': `Bearer ${localStorage.getItem('access_token')}`, 
                      'Content-Type': 'application/json' 
                      }
        });
        const userData = await userRes.json();

        // ذخیره نقش در localStorage
        localStorage.setItem('role', userData.role);
        localStorage.setItem('user_id', userData.id);

        console.log('USER DATA:', userData);


        // ریدایرکت بر اساس نقش
        if (userData.role === 'admin') {
            window.location.href = './adminpanel.html';
        } else if (userData.role === 'student') {
            window.location.href = './studentpanel.html';
        } else {
            window.location.href = './profpanel.html';
        }

    } catch (err) {
        console.error(err);
        errorMsg.textContent = 'خطا در ارتباط با سرور';
        errorMsg.style.display = 'block';
    }
});
