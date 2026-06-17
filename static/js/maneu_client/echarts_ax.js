var myChart = echarts.init(document.getElementById('main1'), 'maneu');
var option = {
    title: {
        text: '眼轴',
        textStyle: {
            fontSize: 18,
            fontWeight: 'bolder',
        },
    },
    tooltip: {},
    legend: {
        data: ['左眼眼轴', '右眼眼轴']
    },
    xAxis: {
        data: ['左眼眼轴', '右眼眼轴'],
    },
    yAxis: {
        name: 'mm',
        min: 15,
        max: 30,
        axisLabel: {
            formatter: function (value, index) {
                return value.toFixed(1)
            }
        }
    },
    series: [{
        type: 'bar',
        barWidth: 20,
        data: [list_r, list_l],
        markLine: {
            data: [{
                label: {
                    formatter: "标准值",
                    fontSize: "10",
                },
                yAxis: stand_ax,
            }],
            silent: true,
            color: ["#99CC33"], // 折线的颜色
        },
    }]
};
// 使用刚指定的配置项和数据显示图表。
myChart.setOption(option);
