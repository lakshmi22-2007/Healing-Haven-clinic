document.getElementById('register-form').addEventListener('submit', function(e) {

  e.preventDefault();

  const userData = {

    name: document.getElementById('name').value,

    email: document.getElementById('email').value,

    phone: document.getElementById('phone').value,

    password: document.getElementById('password').value,

  };



  axios.post('http://localhost:5000/api/register', userData)

    .then(response => alert(response.data.message))

    .catch(error => console.error(error));

});



// Login user

document.getElementById('login-form').addEventListener('submit', function(e) {

  e.preventDefault();

  const loginData = {

    email: document.getElementById('login-email').value,

    password: document.getElementById('login-password').value,

  };



  axios.post('http://localhost:5000/api/login', loginData)

    .then(response => {

      localStorage.setItem('token', response.data.access_token);

      alert('Logged in successfully!');

      loadDoctors();

    })

    .catch(error => alert('Invalid login credentials'));

});



// Load doctor profiles

function loadDoctors() {

  axios.get('http://localhost:5000/api/doctors')

    .then(response => {

      const doctorList = document.getElementById('doctor-list');

      const doctorSelect = document.getElementById('doctor-select');

      response.data.forEach(doc => {

        const listItem = document.createElement('li');

        listItem.textContent = ${doc.name} - ${doc.specialization};

        doctorList.appendChild(listItem);



        const option = document.createElement('option');

        option.value = doc.id;

        option.textContent = ${doc.name} - ${doc.specialization};

        doctorSelect.appendChild(option);

      });

    })

    .catch(error => console.error(error));

}



// Book appointment

document.getElementById('book-appointment-btn').addEventListener('click', function() {

  const appointmentData = {

    doctor_id: document.getElementById('doctor-select').value,

    appointment_time: document.getElementById('appointment-time').value,

  };



  const token = localStorage.getItem('token');



  axios.post('http://localhost:5000/api/book-appointment', appointmentData, {

    headers: { Authorization: Bearer ${token} }

  })

    .then(response => alert(response.data.message))

    .catch(error => console.error(error));

});
