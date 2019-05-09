const checkLogin = () => {
	console.log(document.location.pathname);
	if (Cookies.get('user') == 'true' && document.location.pathname == '/pages/login.html') {
		document.location.replace('/index.html');
		console.log('already logged in');
	} else if (Cookies.get('user') == 'true') {
		console.log('nothing happening, ur logged in n shit');
		return;
	} else if (Cookies.get('user') != 'true' && document.location.pathname != '/pages/login.html') {
		document.location.replace('/pages/login.html');
		console.log('u gotta log in');
	} else {
		console.alert('error: idk fam');
	}
};

const listenToLogout = () => {
	const button = document.getElementById('logout');
	button.addEventListener('click', () => {
		Cookies.remove('user');
		checkLogin();
	});
};

document.addEventListener('DOMContentLoaded', function() {
	console.info('DOM geladen');
	//checkLogin();
	listenToLogout();
});
