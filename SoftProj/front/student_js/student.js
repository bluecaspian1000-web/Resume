
/*
const token = localStorage.getItem('access_token');
const user = JSON.parse(localStorage.getItem('user'));
const studentId = user.id; 
*/

// فعال کردن باز و بسته شدن خودکار زیرمنوها
document.querySelectorAll('.menu-item').forEach(item => {
  const targetId = item.getAttribute('data-target');
  if (!targetId) return;

  item.addEventListener('click', () => {
    const menu = document.getElementById(targetId);
    if (!menu) return;

    // بستن بقیه submenu ها
    document.querySelectorAll('.submenu').forEach(sm => {
      if (sm !== menu) sm.style.display = 'none';
    });

    // باز یا بسته کردن همین منو
    menu.style.display = (menu.style.display === 'block') ? 'none' : 'block';
  });
});




// ---------------- coursesList ------------------
async function renderOferedCourseList() {
  content.innerHTML = `
    <h2>لیست دروس ارائه شده</h2>
    <input type="text" id="searchInput" placeholder="جستجو بر اساس نام درس، کد یا استاد..." style="width: 100%; padding: 10px; margin-bottom: 20px; border-radius: 8px; border: 1px solid #ccc;">
    <div class="offered-container"></div>
  `;

  const container = document.querySelector('.offered-container');
  const searchInput = document.getElementById('searchInput');

  async function render(query = '') {
    container.innerHTML = '';
    try {
      const data = await fetchOfferedCourses(query);

      data.forEach(c => {
        const prof = typeof c.prof === 'string'
          ? c.prof
          : (c.prof?.first_name ? `${c.prof.first_name} ${c.prof.last_name}` : 'نامشخص');

        const semester = typeof c.semester === 'string'
          ? c.semester
          : (c.semester?.code || '---');

        const courseName = c.course?.name || 'نامشخص';
        const courseCode = c.course?.code || '---';
        const group = c.group_code || '---';
        const capacity = c.capacity || '---';

        const sessions = c.sessions?.length
          ? c.sessions.map(s => (s.day_of_week ? `${s.day_of_week} (${s.time_slot})` : s)).join(', ')
          : 'ندارد';

        const card = document.createElement('div');
        card.className = 'offered-card';
        card.innerHTML = `
          <h3>${courseName} (${courseCode})</h3>
          <p><strong>گروه:</strong> ${group}</p>
          <p><strong>استاد:</strong> ${prof}</p>
          <p><strong>ظرفیت:</strong> ${capacity}</p>
          <p><strong>ترم:</strong> ${semester}</p>
          <p><strong>جلسات:</strong> ${sessions}</p>
        `;

        card.addEventListener('click', () => showCourseOfferingDetails(c));
        container.appendChild(card);
      });
    } catch(err) {
      console.error(err);
      alert('خطا در دریافت داده‌ها');
    }
  }

  render();

  let typingTimer;
  searchInput.addEventListener('input', (e) => {
    clearTimeout(typingTimer);
    typingTimer = setTimeout(() => {
      const query = e.target.value.trim();
      render(query);
    }, 300);
  });
}

async function fetchOfferedCourses(query = '') {
  let url = `${API}/courseofferings/`;
  if(query) {
    const params = new URLSearchParams();
    params.append('search', query);
    url += `?${params.toString()}`;
  }
  const res = await fetch(url);
  if(!res.ok) throw new Error('خطا در دریافت داده‌ها');
  return await res.json();
}

// نمایش جزئیات کامل درس ارائه شده + پیشنیازها
function showCourseOfferingDetails(offering) {
  const course = offering.course;

  content.innerHTML = `
    <div class="offered-detail-card">
      <h2>جزئیات درس ارائه شده</h2>

      <p><strong>نام درس:</strong> ${course.name}</p>
      <p><strong>کد درس:</strong> ${course.code}</p>
      <p><strong>واحد:</strong> ${course.unit}</p>
      <p><strong>گروه:</strong> ${offering.group_code}</p>
      <p><strong>ترم:</strong> ${offering.semester}</p>
      <p><strong>استاد:</strong> ${offering.prof ? `${offering.prof.first_name} ${offering.prof.last_name}` : 'نامشخص'}</p>
      <p><strong>ظرفیت:</strong> ${offering.capacity}</p>

      <h4>جلسات</h4>
      <ul>
        ${offering.sessions.length
          ? offering.sessions.map(s => `<li>${s.day_of_week || 'روز نامشخص'} (${s.time_slot || 'زمان نامشخص'}) - ${s.location || 'مکان نامشخص'}</li>`).join('')
          : '<li>ندارد</li>'}
      </ul>

      <h4>پیش‌نیازها</h4>
      <ul>
        ${course.prerequisites.length
          ? course.prerequisites.map(p => `<li>${p.name} (${p.code})</li>`).join('')
          : '<li>ندارد</li>'}
      </ul>

      <button onclick="renderOferedCourseList()">بازگشت</button>
    </div>
  `;
}


// ---------------- coursesList با دکمه اخذ درس ------------------
async function renderEnrollCourseList() {
    const content = document.getElementById('content');
    content.innerHTML = '<h2>انتخاب واحد</h2>';

    try {
        const response = await fetch(`${API}/courseofferings/`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error('خطا در دریافت دروس ارائه شده');
        }

        const courses = await response.json();

        if (!courses.length) {
            content.innerHTML += '<p>هیچ درسی ارائه نشده است.</p>';
            return;
        }

        // جدول دروس ارائه شده
        const table = document.createElement('table');
        table.className = 'course-table';
        table.innerHTML = `
            <thead>
                <tr>
                    <th>گروه</th>
                    <th>کد درس</th>
                    <th>نام درس</th>
                    <th>واحد</th>
                    <th>عملیات</th>
                </tr>
            </thead>
            <tbody></tbody>
        `;

        const tbody = table.querySelector('tbody');

        courses.forEach(course => {
            const tr = document.createElement('tr');
            tr.className = 'course-row';
            tr.innerHTML = `
                <td>${course.group_code || 'نامشخص'}</td>
                <td>${course.course.code}</td>
                <td>${course.course.name}</td>
                <td>${course.course.unit}</td>
                <td>
                    <button class="enroll-btn" data-id="${course.id}">
                        اخذ
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });

        content.appendChild(table);

        // event listener اخذ درس
        document.querySelectorAll('.enroll-btn').forEach(button => {
            button.addEventListener('click', async () => {
                const courseOfferingId = button.getAttribute('data-id');
                button.disabled = true;
                button.textContent = 'در حال ثبت...';

                try {
                    const res = await fetch(`${API}/student-course/enroll/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        },
                        body: JSON.stringify({
                            course_offering_id: courseOfferingId
                        })
                    });

                    if (res.ok) {
                        const result = await res.json();
                        alert(`درس ${result.course_offering.course.name} با موفقیت اخذ شد`);
                        button.textContent = 'اخذ شد';
                        button.classList.add('enrolled');
                    } else {
                        const errorData = await res.json();
                        alert('خطا: ' + JSON.stringify(errorData));
                        button.disabled = false;
                        button.textContent = 'اخذ';
                    }
                } catch (err) {
                    console.error(err);
                    alert('خطا در ثبت درس');
                    button.disabled = false;
                    button.textContent = 'اخذ';
                }
            });
        });

    } catch (error) {
        console.error(error);
        content.innerHTML += '<p>خطا در دریافت اطلاعات دروس.</p>';
    }
}



// --------- دروس اخذ شده -----------------  
// enrolled-courses.js

async function renderEnrolledCourses() {
    const content = document.getElementById('content');
    content.innerHTML = '<h2>دروس اخذ شده</h2>';

    // جدول
    const table = document.createElement('table');
    table.className = 'enrolled-table';
    table.innerHTML = `
        <thead>
            <tr>
                <th>گروه</th>
                <th>کد درس</th>
                <th>نام درس</th>
                <th>واحد</th>
                <th>سشن‌ها</th>
                <th>استاد</th>
                <th>عملیات</th>
            </tr>
        </thead>
        <tbody></tbody>
    `;
    const tbody = table.querySelector('tbody');
    content.appendChild(table);

    try {
        // GET دروس اخذ شده ترم فعال
        const response = await fetch(`${API}/student-course/`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) throw new Error('خطا در دریافت دروس اخذ شده');

        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            throw new Error('سرور JSON برنگرداند');
        }

        const enrolledCourses = await response.json();

        if (!enrolledCourses.length) {
            content.innerHTML += '<p style="text-align:center;color:#e74c3c;">درسی اخذ نشده است.</p>';
            return;
        }

        // نمایش دروس
        for (const item of enrolledCourses) {
            const tr = document.createElement('tr');

            // سشن‌ها
            const sessionsText = (item.course_offering?.sessions || [])
                .map(s => `${s.day_of_week} (${s.time_slot})${s.location ? ' - ' + s.location : ''}`)
                .join(', ') || 'نامشخص';

            // نام استاد
            const instructorName = item.course_offering?.prof
                ? `${item.course_offering.prof.first_name} ${item.course_offering.prof.last_name}`
                : 'نامشخص';

            tr.innerHTML = `
                <td>${item.course_offering?.group_code || 'نامشخص'}</td>
                <td>${item.course_offering?.course?.code || 'نامشخص'}</td>
                <td>${item.course_offering?.course?.name || 'نامشخص'}</td>
                <td>${item.course_offering?.course?.unit || 0}</td>
                <td>${sessionsText}</td>
                <td>${instructorName}</td>
                <td>
                    <button class="drop-btn" data-id="${item.id}">حذف</button>
                </td>
            `;
            tbody.appendChild(tr);

            // حذف درس
            tr.querySelector('.drop-btn').addEventListener('click', async () => {
                try {
                    if (!confirm('آیا از حذف این درس مطمئن هستید؟')) return;

                    const deleteRes = await fetch(`${API}/student-course/${item.id}/`, {
                        method: 'DELETE',
                        headers: { 'Authorization': `Bearer ${token}` }
                    });

                    if (deleteRes.ok) {
                        tr.remove();
                    } else {
                        const errData = await deleteRes.json();
                        alert('خطا در حذف درس: ' + JSON.stringify(errData));
                    }
                } catch (err) {
                    console.error(err);
                    alert('خطا در حذف درس');
                }
            });
        }

    } catch (err) {
        console.error(err);
        content.innerHTML += '<p style="text-align:center;color:#e74c3c;">خطا در بارگذاری دروس اخذ شده</p>';
    }
}

/*
async function renderEnrolledCourses() {
    const content = document.getElementById('content');
    content.innerHTML = '<h2>دروس اخذ شده</h2>';

    // جدول
    const table = document.createElement('table');
    table.className = 'enrolled-table';
    table.innerHTML = `
        <thead>
            <tr>
                <th>گروه</th>
                <th>کد درس</th>
                <th>نام درس</th>
                <th>واحد</th>
                <th>سشن‌ها</th>
                <th>استاد</th>
                <th>عملیات</th>
            </tr>
        </thead>
        <tbody></tbody>
    `;
    const tbody = table.querySelector('tbody');
    content.appendChild(table);

    try {
        // ===== GET دروس اخذ شده ترم فعال =====
        const response = await fetch(`${API}/student-course/`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error('خطا در دریافت دروس اخذ شده');
        }

        // بررسی Content-Type قبل از parse
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            throw new Error('سرور JSON برنگرداند');
        }

        const enrolledCourses = await response.json();

        if (!enrolledCourses.length) {
            content.innerHTML += '<p>درسی اخذ نشده است.</p>';
            return;
        }

        // ===== نمایش دروس =====
        for (const item of enrolledCourses) {
            try {
                const tr = document.createElement('tr');

                // نمایش سشن‌ها
               const sessionsText = (item.course_offering?.sessions || [])
                  .map(s => `${s.day_of_week} (${s.time_slot})${s.location ? ' - ' + s.location : ''}`)
                  .join(', ') || 'نامشخص';


                // نام استاد
                const instructorName = item.course_offering?.prof
                    ? `${item.course_offering.prof.first_name} ${item.course_offering.prof.last_name}`
                    : 'نامشخص';

                tr.innerHTML = `
                    <td>${item.course_offering?.group_code || 'نامشخص'}</td>
                    <td>${item.course_offering?.course?.code || 'نامشخص'}</td>
                    <td>${item.course_offering?.course?.name || 'نامشخص'}</td>
                    <td>${item.course_offering?.course?.unit || 0}</td>
                    <td>${sessionsText}</td>
                    <td>${instructorName}</td>
                    <td>
                        <button 
                            class="drop-btn"
                            style="background:red;color:white"
                            data-id="${item.id}">
                            حذف
                        </button>
                    </td>
                `;
                tbody.appendChild(tr);

                // ===== حذف درس =====
                tr.querySelector('.drop-btn').addEventListener('click', async () => {
                    try {
                        if (!confirm('آیا از حذف این درس مطمئن هستید؟')) return;

                        const deleteRes = await fetch(`${API}/student-course/${item.id}/`, {
                            method: 'DELETE',
                            headers: {
                                'Authorization': `Bearer ${token}`
                            }
                        });

                        if (deleteRes.ok) {
                            tr.remove();
                        } else {
                            const errData = await deleteRes.json();
                            alert('خطا در حذف درس: ' + JSON.stringify(errData));
                        }
                    } catch (err) {
                        console.error(err);
                        alert('خطا در حذف درس');
                    }
                });

            } catch (err) {
                console.error('خطا در رندر یک درس:', err);
            }
        }

    } catch (err) {
        console.error(err);
        content.innerHTML += '<p>خطا در بارگذاری دروس اخذ شده</p>';
    }
}
*/