var myChart = echarts.init(document.getElementById('main0'), 'maneu');
var option = {
    title: {
        text: '视力',
        textStyle: {
            fontSize: 18,
            fontWeight: 'bolder',
        },
    },
    tooltip: {},
    legend: {
        data: ['右眼']
    },
    xAxis: {
        data: ['左眼视力', '右眼视力'],
    },
    yAxis: {
        min: 0.2,
        max: 1.2,
        axisLabel: {
            formatter: function (value, index) {
                return value.toFixed(1)
            }
        }
    },
    series: [{
        type: 'bar',
        barWidth: 20,
        data: [OS_VA, OD_VA],
        markLine: {
            data: [{
                label: {
                    formatter: "标准视力",
                    fontSize: "10",
                },
                yAxis: 1.0,
            }],
            silent: true,
        }
    }]
};
// 使用刚指定的配置项和数据显示图表。
myChart.setOption(option);
