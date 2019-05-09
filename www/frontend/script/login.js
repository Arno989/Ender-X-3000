'use strict';

//#region callback
const logUserIn = user => {
	const password = document.getElementById('loginPassword').value;
	const error = document.querySelector('.error');
	try {
		if (user[0].password == password) {
			Cookies.set('user', 'true', { expires: 1 } /*, {secure : true}*/);
			document.location.replace('/index.html');
		} else {
			error.style.display = 'block';
			error.innerHTML = 'Incorrect login information';
		}
	} catch {
		error.style.display = 'block';
		error.innerHTML = 'User doesnt exist';
	}
};

const registerUser = () => {
	Cookies.set('user', 'true', { expires: 1 } /*, {secure : true}*/);
	document.location.replace('/index.html');
};
//#endregion

//#region ListenTo
const listenToLogin = () => {
	const button = document.getElementById('login');
	button.addEventListener('click', () => {
		const username = document.getElementById('loginUsername').value;

		handleData(`http://127.0.0.1:5000/api/v1/users/${username}`, logUserIn);
	});
};

const listenToRegister = () => {
	const button = document.getElementById('create');
	button.addEventListener('click', () => {
		const username = document.getElementById('registerUsername').value;
		const password = document.getElementById('registerPassword').value;

		let json = `{
			"username" : "${username}",
			"password" : "${password}"
		}`;

		handleData(`http://127.0.0.1:5000/api/v1/users`, registerUser, 'POST', json);
		console.log(json);
	});
};
//#endregion

//#region init
const init = function() {
	listenToLogin();
	listenToRegister();
};

document.addEventListener('DOMContentLoaded', function() {
	console.info('DOM geladen');
	init();
});
//#endregion
