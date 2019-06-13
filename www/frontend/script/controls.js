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

	const btns = document.querySelectorAll('.js-button-distance');

	const value = document.querySelector('.js-value');
	const extrude = document.querySelector('.js-extrude');
	const retract = document.querySelector('.js-retract');

	const motorsOff = document.querySelector('.js-motorsoff');
	const fanOn = document.querySelector('.js-fanon');
	const fanOff = document.querySelector('.js-fanoff');

	xyUp.addEventListener('click', () => {
		socket.emit('X', distance, true);
	});

	xyLeft.addEventListener('click', () => {
		socket.emit('Y', distance, false);
	});

	xyHome.addEventListener('click', () => {
		socket.emit('xy-home');
	});

	xyRight.addEventListener('click', () => {
		socket.emit('Y', distance, true);
	});

	xyDown.addEventListener('click', () => {
		socket.emit('X', distance, false);
	});

	zUp.addEventListener('click', () => {
		socket.emit('Z', distance, true);
	});

	zHome.addEventListener('click', () => {
		socket.emit('z-home');
	});

	zDown.addEventListener('click', () => {
		socket.emit('Z', distance, false);
	});

	for (const btn of btns) {
		btn.addEventListener('click', () => {
			distance = btn.getAttribute('value');
		});
	}

	extrude.addEventListener('click', () => {
		socket.emit('E', value.getAttribute('value'), true);
		console.log(value.getAttribute('value'));
	});

	retract.addEventListener('click', () => {
		socket.emit('E', value.getAttribute('value'), false);
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
	enableSocketIo();
	enablestream();
	listenToControls();
};

document.addEventListener('DOMContentLoaded', init);
//#endregion
