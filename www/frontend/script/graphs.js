'use strict';
Chart.defaults.global.elements.point.radius = 0;
Chart.defaults.global.elements.line.borderWidth = 2;
Chart.defaults.global.legend.position = 'top';

const socket_IP = `${window.location.host}:5000`;

const showPrinterTemp = jsonObject => {
	let json = {
		labels: [],
		data: {
			enclosure: [],
			bed: [],
			hotend: []
		}
	};

	for (const i of jsonObject) {
		console.log(jsonObject);
		const timestamp = new Date(i.timestamp);
		json.labels.push(`${timestamp.getHours()}:${String(timestamp.getMinutes()).padStart(2, '0')}`);

		if (i.sensor == 'ta') {
			json.data.enclosure.push(i.value);
		} else if (i.sensor == 'tb') {
			json.data.bed.push(i.value);
		} else if (i.sensor == 'th') {
			json.data.hotend.push(i.value);
		}
	}

	var printerTemp = document.getElementById('printerTemp').getContext('2d');
	var printerTempChart = new Chart(printerTemp, {
		type: 'line',
		data: {
			labels: ['-50s', '-45s', '-40s', '-35s', '-30s', '-25s', '-20s', '-15s', '-10s', '-05s', '+0s'],
			datasets: [
				{
					label: 'Enclosure',
					backgroundColor: 'rgb(255, 255, 255, 0)',
					borderColor: 'rgb(255, 99, 132)',
					data: json.data.enclosure,
					spanGaps: true
				},
				{
					label: 'Bed',
					backgroundColor: 'rgb(255, 255, 255, 0)',
					borderColor: 'rgb(66, 179, 244)',
					data: json.data.bed,
					spanGaps: true
				},
				{
					label: 'Hotend',
					backgroundColor: 'rgb(255, 255, 255, 0)',
					borderColor: 'rgb(86, 244, 65)',
					data: json.data.hotend,
					spanGaps: true
				}
			]
		},
		options: {
			legend: {
				labels: {
					boxWidth: 0.5
				}
			},
			scales: {
				xAxes: [
					{
						gridLines: {
							display: false
						}
					}
				],
				yAxes: [
					{
						gridLines: {
							display: true,
							lineWidth: 0.5
						},
						ticks: {
							max: 250,
							stepSize: 20,
							suggestedMin: 0,
							suggestedMax: 100
						}
					}
				]
			}
		}
	});
};

const showHumidity = jsonObject => {
	let json = {
		labels: [],
		data: {
			printer: [],
			fillament: []
		}
	};

	for (const i of jsonObject) {
		const timestamp = new Date(i.timestamp);
		json.labels.push(`${timestamp.getHours()}:${String(timestamp.getMinutes()).padStart(2, '0')}`);

		if (i.sensor == 'hp') {
			json.data.printer.push(i.value);
			json.data.fillament.push(null);
		} else if (i.sensor == 'hf') {
			json.data.printer.push(null);
			json.data.fillament.push(i.value);
		}
	}

	var humidity = document.getElementById('humidity').getContext('2d');
	var humidityChart = new Chart(humidity, {
		type: 'line',
		data: {
			labels: json.labels,
			datasets: [
				{
					label: 'Printer',
					backgroundColor: 'rgb(255, 255, 255, 0)',
					borderColor: 'rgb(255, 99, 132)',
					data: json.data.printer,
					spanGaps: true
				},
				{
					label: 'Fillament',
					backgroundColor: 'rgb(255, 255, 255, 0)',
					borderColor: 'rgb(66, 179, 244)',
					data: json.data.fillament,
					spanGaps: true
				}
			]
		},
		options: {
			legend: {
				labels: {
					boxWidth: 0.5
				}
			},
			scales: {
				xAxes: [
					{
						gridLines: {
							display: false
						}
					}
				],
				yAxes: [
					{
						gridLines: {
							display: true,
							lineWidth: 0.5
						},
						ticks: {
							min: 0,
							max: 100,
							stepSize: 10,
							suggestedMin: 0,
							suggestedMax: 50
						}
					}
				]
			}
		}
	});
};

const showGasData = jsonObject => {
	let json = {
		labels: [],
		data: {
			co2: [],
			tvoc: []
		}
	};

	for (const i of jsonObject) {
		const timestamp = new Date(i.timestamp);
		json.labels.push(`${timestamp.getHours()}:${String(timestamp.getMinutes()).padStart(2, '0')}`);

		if (i.sensor == 'co2') {
			json.data.co2.push(i.value);
		} else if (i.sensor == 'tvo') {
			json.data.tvoc.push(i.value);
		}
	}

	var tvoc = document.getElementById('tvoc').getContext('2d');
	var tvocChart = new Chart(tvoc, {
		type: 'line',
		data: {
			labels: json.labels,
			datasets: [
				{
					label: 'CO2',
					yAxisID: 'A',
					backgroundColor: 'rgb(255, 255, 255, 0)',
					borderColor: 'rgb(255, 99, 132)',
					data: json.data.co2,
					spanGaps: true
				},
				{
					label: 'TVOC',
					yAxisID: 'B',
					backgroundColor: 'rgb(255, 255, 255, 0)',
					borderColor: 'rgb(66, 179, 244)',
					data: json.data.tvoc,
					spanGaps: true
				}
			]
		},
		options: {
			legend: {
				labels: {
					boxWidth: 0.5
				}
			},
			scales: {
				xAxes: [
					{
						gridLines: {
							display: false
						}
					}
				],
				yAxes: [
					{
						gridLines: {
							display: true,
							lineWidth: 0.5,
							color: 'rgb(255, 99, 132)'
						},
						id: 'A',
						position: 'left',
						ticks: {
							max: 8192,
							min: 400
						}
					},
					{
						gridLines: {
							display: true,
							lineWidth: 0.5,
							color: 'rgb(66, 179, 244)'
						},
						id: 'B',
						position: 'right',
						ticks: {
							max: 1187,
							min: 0
						}
					}
				]
			}
		}
	});
};

const getPrinterTempData = () => {
	handleData(`http://${socket_IP}/api/v1/data/printer/temp`, showPrinterTemp);
};

const getHumidityData = () => {
	handleData(`http://${socket_IP}/api/v1/data/humid`, showHumidity);
};

const getGasData = () => {
	handleData(`http://${socket_IP}/api/v1/data/printer/gas`, showGasData);
};

document.addEventListener('DOMContentLoaded', function() {
	console.info('DOM geladen');
	getPrinterTempData();
	getHumidityData();
	getGasData();
});
