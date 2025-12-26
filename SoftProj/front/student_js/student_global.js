

const token = localStorage.getItem('access_token');
const user = JSON.parse(localStorage.getItem('user') || '{}');
const studentId = user.id || null;

//const user = JSON.parse(localStorage.getItem('user'));
//const studentId = user.id; 
