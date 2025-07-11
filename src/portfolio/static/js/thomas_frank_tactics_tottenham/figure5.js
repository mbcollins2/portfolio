document.addEventListener('DOMContentLoaded', () => {

    Chart.defaults.global.defaultFontFamily = "'Gaegu'";
    Chart.defaults.global.title.display = true;
    Chart.defaults.global.title.fontColor = '#FFF';
    Chart.defaults.global.legend.labels.fontColor = '#FFF';
    Chart.defaults.scale.ticks.fontColor = '#FFF';
    Chart.defaults.scale.scaleLabel.display = true;
    Chart.defaults.scale.scaleLabel.fontColor = '#FFF';


    Chart.plugins.register(ChartRough);
    var fontObserver = new FontFaceObserver('Gaegu');
    fontObserver.load().then(function () {
        function getResponsiveFontSizes() {
            const isMobile = window.innerWidth < 768;
            return {
                title: isMobile ? 18 : 24,
                legend: isMobile ? 12 : 18,
                scaleLabel: isMobile ? 14 : 20,
                ticks: isMobile ? 12 : 18,
            };
        };
        const initialFontSizes = getResponsiveFontSizes();
        const ctx = document.getElementById('figure5').getContext('2d');
        const myChart = new Chart(ctx, {
            type: 'horizontalBar',
            data: {
                labels: ['Top Half','Bottom Half'],
                datasets: [{
                    label: '# of Different Formations Used',
                    data: [7,3],
                    backgroundColor: '#8787BB',
                    borderColor: '#fff',
                    borderWidth: 1,
                    rough: {
                        roughness: 1,
                        fillStyle: 'hachure',
                        fillWeight: 0.8,
                    }
                }]
            },
            options: {
                maintainAspectRatio: false,
                animation: false,
                onResize: function(chart, size) {
                    const newFontSizes = getResponsiveFontSizes();
                    chart.options.title.fontSize = newFontSizes.title;
                    chart.options.legend.labels.fontSize = newFontSizes.legend;
                    chart.options.scales.yAxes[0].ticks.fontSize = newFontSizes.ticks;
                    chart.options.scales.xAxes[0].ticks.fontSize = newFontSizes.ticks;
                    chart.options.scales.yAxes[0].scaleLabel.fontSize = newFontSizes.scaleLabel;
                    chart.options.scales.xAxes[0].scaleLabel.fontSize = newFontSizes.scaleLabel;
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true,
                            fontSize: initialFontSizes.ticks
                        },
                        scaleLabel: {
                            labelString: 'Opponent Quality',
                            fontSize: initialFontSizes.scaleLabel
                        }
                    }],
                    xAxes: [{
                        ticks: {
                            beginAtZero: true,
                            fontSize: initialFontSizes.ticks,
                            max: 8,
                        },
                        scaleLabel: {
                            labelString: '# of Different Formations Used',
                            fontSize: initialFontSizes.scaleLabel
                        }
                    }],
                },
                legend: {
                    labels: {
                        fontColor: '#fff',
                        fontSize: initialFontSizes.legend
                    }
                },
                title: {
                    text: ["Thomas Frank Formations by Opp. Quality", "('23-24 Seasons)"],
                    fontSize: initialFontSizes.title,
                },
                layout: {
                    padding: {
                        right: 10,
                        left: 10,
                    }
                }
            }
        });
    });
});
