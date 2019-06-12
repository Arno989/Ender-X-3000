'use strict';

const socket_IP = `${window.location.host}:5000`;

let socket;

var distance = 10;
//#region ***********  Callback - HTML Generation (After select) ***********

//#endregion

//#region ***********  Data Access ***********
const enablestream = () => {
	const element = document.querySelector('.js-video');
	element.setAttribute('src', `http://${window.location.host}:8080/0/stream`);
};
//#endregion

//#region ***********  Event Listeners ***********
const listenToControls = () => {
	const xyUp = document.querySelector('.js-xy-up');
	const xyLeft = document.querySelector('.js-xy-left');
	const xyHome = document.querySelector('.js-xy-home');
	const xyRight = document.querySelector('.js-xy-right');
	const xyDown = document.querySelector('.js-xy-down');

	const zUp = document.querySelector('.js-z-up');
	const zHome = document.querySelector('.js-z-home');
	const zDown = document.querySelector('.js-z-down');

	const btns = document.querySelector('.c-button--distance');

	const value = document.querySelector('.js-value');
	const extrude = document.querySelector('.js-extrude');
	const retract = document.querySelector('.js-retract');

	const motorsOff = document.querySelector('.js-motorsoff');
	const fanOn = document.querySelector('.js-fanon');
	const fanOff = document.querySelector('.js-fanoff');

	xyUp.addEventListener('click', () => {
		socket.emit('xy-up', distance);
	});

	xyLeft.addEventListener('click', () => {
		socket.emit('xy-left', distance);
	});

	xyHome.addEventListener('click', () => {
		socket.emit('xy-home', distance);
	});

	xyRight.addEventListener('click', () => {
		socket.emit('xy-right', distance);
	});

	xyDown.addEventListener('click', () => {
		socket.emit('xy-down', distance);
	});

	zUp.addEventListener('click', () => {
		socket.emit('z-up', distance);
	});

	zHome.addEventListener('click', () => {
		socket.emit('z-home', distance);
	});

	zDown.addEventListener('click', () => {
		socket.emit('z-down', distance);
	});

	for (const btn in btns) {
		btn.addEventListener('click', () => {
			distance = btn.getAttribute('value');
		});
	}

	extrude.addEventListener('click', () => {
		socket.emit('extrude', value.getAttribute('value'));
		console.log(value.getAttribute('value'));
	});

	retract.addEventListener('click', () => {
		socket.emit('retract', value.getAttribute('value'));
	});

	motorsOff.addEventListener('click', () => {
		socket.emit('motorsoff');
	});

	fanOn.addEventListener('click', () => {
		socket.emit('fanon');
	});

	fanOff.addEventListener('click', () => {
		socket.emit('fanoff');
	});
};
//#endregion

//#region ***********  INIT / DOMContentLoaded ***********
const enableSocketIo = () => {
	socket = io(`http://${socket_IP}`);
};

const init = function() {
	console.log('bitch ass');
	enableSocketIo();
	enablestream();
	listenToControls();
};

document.addEventListener('DOMContentLoaded', init);
//#endregion
