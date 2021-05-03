window.onresize = function () {

    myChart.resize();
}
$.ajaxSetup({async: false});
// 基于准备好的容器(这里的容器是id为myChart的div)，初始化echarts实例
var myChart = echarts.init(document.getElementById("guanxi"));
myChart.showLoading();

myChart.hideLoading();

function setChart(symbolSize, fontSize, nodes, links) {

    option = {
        // backgroundColor: "white",        // 背景颜色
        title: {                            //图表标题
            // text: '知识图谱',                  // 标题文本
            textStyle: {                        // 标题样式
                // color: "white",                    // 标题字体颜色
                fontWeight: "lighter",                // 定义更细的字符
            }
        },
        animationDurationUpdate: 1500,              // 数据更新动画的时长。[ default: 300 ]
        animationEasingUpdate: 'quinticInOut',      // 数据更新动画的缓动效果。[ default: cubicOut ]
        legend: {                              //图表控件
            x: "center",
            show: true, //默认显示
            data: ["一级概念", "二级概念", "三级概念", "四级概念", "五级概念", "函数", "重要程度"]
        },
        series: [
            {
                type: 'graph',                          // 关系图
                layout: 'force',                        // 布局
                symbolSize: symbolSize,
                edgeSymbol: ['circle', 'arrow'],
                edgeSymbolSize: [4, 4],
                edgeLabel: {
                    normal: {
                        show: true,
                        textStyle: {
                            fontSize: 10
                        },
                        formatter: "{c}"
                    }
                },
                force: {
                    repulsion: 2500,        // [ default: 50 ]节点之间的斥力因子(关系对象之间的距离)。支持设置成数组表达斥力的范围，此时不同大小的值会线性映射到不同的斥力。值越大则斥力越大
                    edgeLength: [10, 100]   // [ default: 30 ]边的两个节点之间的距离(关系对象连接线两端对象的距离,会根据关系对象值得大小来判断距离的大小)，
                },
                focusNodeAdjacency: true,   // 是否在鼠标移到节点上的时候突出显示节点以及节点的边和邻接节点。[ default: false ]
                draggable: true,
                roam: true,                 // 是否开启鼠标缩放和平移漫游。默认不开启。如果只想要开启缩放或者平移，可以设置成 'scale' 或者 'move'。设置成 true 为都开启
                categories: [{               // 节点分类的类目，可选
                    name: '一级概念',               // 类目名称，用于和 legend 对应以及格式化 tooltip 的内容。
                    // itemStyle: {
                    //     normal: {
                    //         color: "#009800",
                    //     }
                    // }
                }, {
                    name: '二级概念',
                }, {
                    name: '三级概念',
                }, {
                    name: '四级概念',
                }, {
                    name: '五级概念',
                }, {
                    name: '函数',
                },
                    {
                        name: '重要程度',
                    }
                ],
                label: {        // 关系对象上的标签
                    normal: {
                        show: true,             // 显示标签
                        //position: "inside",     // 标签位置
                        textStyle: {              // 文本样式
                            fontSize: fontSize
                        },
                    }
                },
                force: {
                    repulsion: 1000
                },
                tooltip: {              // 提示框配置
                    formatter: function (node) { // 区分连线和节点，节点上额外显示其他数字
                        if (!node.value) {
                            return node.data.name;
                        } else {
                            return node.data.name + ":" + node.data.showNum;
                        }
                    },
                },
                lineStyle: {
                    normal: {
                        opacity: 0.9,
                        width: 1,
                        curveness: 0.3
                    }
                },
                // progressiveThreshold: 700,
                nodes: nodes,
                links: links,
            }
        ]
    };
}

