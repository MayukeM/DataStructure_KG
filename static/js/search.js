function search(name) {
    $.getJSON('/search_name', {
        name: name,
    }, function (json) {
        option.series[0].nodes = json.data.map(function (node, idx) {
            node.id = idx;
            return node;
        });
        option.series[0].links = json.links;
        // 使用刚指定的配置项和数据显示图表
        myChart.setOption(option, true);
    });
}

function search_branch(name, deep) {

    $.getJSON('/search_branch', {
        name: name,
        deep: deep,
    }, function (json) {

        option.series[0].nodes = json.data.map(function (node, idx) {
            node.id = idx;
            return node;
        });

        option.series[0].links = json.links;

        // 使用刚指定的配置项和数据显示图表
        myChart.setOption(option, true);

    });
}

function search_path(a, b) {
    $.getJSON('/search_path', {
        a: a,
        b: b,
    }, function (json) {
        option.series[0].nodes = json.data.map(function (node, idx) {
            node.id = idx;
            return node;
        });
        option.series[0].links = json.links;
        // 使用刚指定的配置项和数据显示图表
        myChart.setOption(option, true);
    });
}

function search_answer() {
    $.getJSON('/KGQA_answer', {
        name: $("#search").val(),
    }, function (json) {
        if (json[0] != undefined) {
            // console.log(json[0])
            // if (json[0] == "[object Object]") {
            //     alert("没有查询到结果，请选择模糊搜索")
            // }
            option.series[0].nodes = json[0].data.map(function (node, idx) {
                node.id = idx;
                return node;
            });
            option.series[0].links = json[0].links;
        } else {
            // console.log(json)
            // if (json == "[object Object]") {
            //     alert("没有查询到结果，请选择模糊搜索")
            // }
            option.series[0].nodes = json.data.map(function (node, idx) {
                node.id = idx;
                return node;
            });
            option.series[0].links = json.links;
        }
        myChart.setOption(option, true);
        // $("#profile").html(json[1]);
        // $("#picture").css("display", "block");
        // $("#picture").attr("src", "data:image/jpg;base64," + json[2]);
    });
}

function search_fuzzy() {
    $.getJSON('/KGQA_fuzzy', {
        name: $("#search").val(),
    }, function (json) {
        $("#fuzzy").html(json);
        $("#fuzzy").css("display", "block");
    });
}

myChart.on('click', function (params) {
    // console.log(params)
    var province = params.name;
    $.getJSON('/get_profile', {
        character_name: province,

    }, function (json) {
        $("#profile").html(json[0]);
        $("#picture").css("display", "block");
        $("#picture").attr("src", "data:image/jpg;base64," + json[1]);
    });
    layer.config({
        extend: '../css/style.css',         //加载您的扩展样式//默认皮肤配置文件是放在css/modal/layer/myskin/style.css
        skin: 'layer-ext-yourskin'          //一旦设定，所有layer弹层风格都采用此主题。
    });
    layer.open({
        title: province,
        type: 1,
        area: ["400px", "650px"],
        closeBtn: 10,               //显示关闭按钮
        maxmin: true,
        shadeClose: true,           // 点击遮罩是否关闭
        shade: 0.1,                 // 遮罩透明度
        skin: 'layer-ext-moon',
        offset: "r",                //从右边弹出
        content: $("#bound").html()
    });
});
