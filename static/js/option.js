window.onresize = function () {

    myChart.resize();
}
$.ajaxSetup({async: false});
// 基于准备好的容器(这里的容器是id为myChart的div)，初始化echarts实例
var myChart = echarts.init(document.getElementById("guanxi"));
myChart.showLoading();

myChart.hideLoading();

option = {
    // backgroundColor: "white",        // 背景颜色
    title: {                            //图表标题
        // text: '知识图谱',                  // 标题文本
        textStyle: {                        // 标题样式
            // color: "white",                    // 标题字体颜色
            fontWeight: "lighter",                // 定义更细的字符
        }
    },
    animationDurationUpdate: false,              // 数据更新动画的时长。[ default: 300 ]
    animationEasingUpdate: false,      // 数据更新动画的缓动效果。[ default: cubicOut ] quinticInOut
    legend: {                              //图表控件
        x: "center",
        show: true, //默认显示
        data: ["一级概念", "二级概念", "三级概念", "四级概念", "五级概念", "六级概念", "函数"]
    },
    series: [
        {
            type: 'graph',                          // 关系图
            layout: 'force',                        // 布局
            legendHoverLink : true,                 //是否启用图例 hover(悬停) 时的联动高亮。
            symbolSize: 30,                         //节点大小
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
                repulsion: 800,        // [ default: 50 ]节点之间的斥力因子(关系对象之间的距离)。支持设置成数组表达斥力的范围，此时不同大小的值会线性映射到不同的斥力。值越大则斥力越大
                edgeLength: [10, 100],   // [ default: 30 ]边的两个节点之间的距离(关系对象连接线两端对象的距离,会根据关系对象值得大小来判断距离的大小)，
                layoutAnimation: true,  //因为力引导布局会在多次迭代后才会稳定，这个参数决定是否显示布局的迭代动画，在浏览器端节点数据较多（>100）的时候不建议关闭，布局过程会造成浏览器假死。
                // gravity:0.1
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
                name: '六级概念',
            }, {
                name: '函数',
            }
            ],
            label: {        // 关系对象上的标签
                normal: {
                    show: true,             // 显示标签
                    position: "right",     // 标签位置
                    textStyle: {              // 文本样式
                        fontSize: 20
                    },
                }
            },
            tooltip: {              // 提示框配置
                trigger:'item',
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
                    curveness: 0,  // 边的曲度
                    color:"target"
                }
            },
            // progressiveThreshold: 700,
            nodes: [],
            links: [],
        }
    ]
};


//base64转blob
function base64ToBlob(code) {
    let parts = code.split(';base64,');
    let contentType = parts[0].split(':')[1];
    let raw = window.atob(parts[1]);
    let rawLength = raw.length;
    let uInt8Array = new Uint8Array(rawLength);
    for (let i = 0; i < rawLength; ++i) {
        uInt8Array[i] = raw.charCodeAt(i);
    }
    return new Blob([uInt8Array], {type: contentType});
}

function saveAsImage() {
    let content = myChart.getDataURL();

    let aLink = document.createElement('a');
    let blob = this.base64ToBlob(content);

    let evt = document.createEvent("HTMLEvents");
    evt.initEvent("click", true, true);
    aLink.download = "graph.png";
    aLink.href = URL.createObjectURL(blob);
    aLink.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true, view: window}));
}