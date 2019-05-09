'use strict';
Chart.defaults.global.elements.point.radius = 0;
Chart.defaults.global.elements.line.borderWidth = 2;
Chart.defaults.global.legend.position = 'top';

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
		const timestamp = new Date(i.timestamp);
		json.labels.push(`${timestamp.getHours()}:${String(timestamp.getMinutes()).padStart(2, '0')}`);

		json.data.enclosure.push(i.enclosure);
		json.data.bed.push(i.bed);
		json.data.hotend.push(i.hotend);
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
					data: json.data.enclosure
				},
				{
					label: 'Bed',
					backgroundColor: 'rgb(255, 255, 255, 0)',
					borderColor: 'rgb(66, 179, 244)',
					data: json.data.bed
				},
				{
					label: 'Hotend',
					backgroundColor: 'rgb(255, 255, 255, 0)',
					borderColor: 'rgb(86, 244, 65)',
					data: json.data.hotend
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
							max: 230,
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

		json.data.printer.push(i.printer);
		json.data.fillament.push(i.fillament);
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
					data: json.data.printer
				},
				{
					label: 'Fillament',
					backgroundColor: 'rgb(255, 255, 255, 0)',
					borderColor: 'rgb(66, 179, 244)',
					data: json.data.fillament
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
							min: -10,
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

		json.data.co2.push(i.co2);
		json.data.tvoc.push(i.tvoc);
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
					data: json.data.co2
				},
				{
					label: 'TVOC',
					yAxisID: 'B',
					backgroundColor: 'rgb(255, 255, 255, 0)',
					borderColor: 'rgb(66, 179, 244)',
					data: json.data.tvoc
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
	handleData(`http://127.0.0.1:5000/api/v1/data/printer/temp`, showPrinterTemp);
};

const getHumidityData = () => {
	handleData(`http://127.0.0.1:5000/api/v1/data/humid`, showHumidity);
};

const getGasData = () => {
	handleData(`http://127.0.0.1:5000/api/v1/data/printer/gas`, showGasData);
};

document.addEventListener('DOMContentLoaded', function() {
	console.info('DOM geladen');
	getPrinterTempData();
	getHumidityData();
	getGasData();
});
