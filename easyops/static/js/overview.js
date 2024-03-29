(function ($) {
  $(document).ready(function () {
    var mapAddressChart = document.getElementById("access_address_source");
    var mapData;
    var mapOption;
    var mapChart;
    axios.get("/api/v1.0/resources/login_info").then(function (response) {
      console.log(response.data.user_login_info);
      mapData = response.data.user_login_info;
    });

    $("overview").on("click");
    axios.get("https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json").then(function (response) {
      var mapChinaJson = response.data;
      // 注册地图
      echarts.registerMap("china", mapChinaJson);
      // 初始化地图
      mapChart = echarts.init(mapAddressChart, "dark", {
        renderer: "canvas",
        useDirtyRect: false,
      });

      mapOption = {
        // 加载地图组件
        title: {
          text: "登陆地展示",
        },
        legend: {
          show: true,
        },
        geo: [
          {
            map: "china", // 使用中国地图
            roam: true, // 允许缩放和平移
            regions: [],
            zoom: 1.8,
            nameProperty: "name",
            label: {
              show: true,
              areaColor: "#ddb926",
              color: "rgba(0,0,0,0.7)",
              fontStyle: "normal",
              fontFamily: "monospace",
              fontSize: 10,
            },
            itemStyle: {
              normal: {
                borderColor: "rgba(0, 0, 0, 0.2)",
              },
              emphasis: {
                areaColor: "#f3b329",
                borderWidth: 0.6,
                shadowOffsetX: 0,
                shadowOffsetY: 0,
                shadowBlur: 20,
                shadowColor: "rgba(0, 0, 0, 0.5)",
              },
            },
          },
        ],
        tooltip: {
          trigger: "item",
          showDelay: 0,
          formatter: function (params) {
            if (params.value) {
              return params.name + "<br />" + params.seriesName + ": " + params.value;
            } else {
              return params.name + "<br />" + params.seriesName + ": " + 0;
            }
          },
        },
        toolbox: {
          feature: {
            saveAsImage: {},
            restore: {},
          },
        },
        visualMap: {
          min: 0,
          max: 100,
          left: "left",
          top: "bottom",
          text: ["极高", "无数据"],
          inRange: {
            color: ["#30ffff", "#006edd"],
          },
          show: true,
        },
        /*     dataRange: {
      //左下角的颜色块。start：值域开始值；end：值域结束值；label：图例名称；color：自定义颜色值
      x: "left",
      y: "bottom",
      splitList: [
        { start: 41, label: "> 41  极高", color: "#b80909" },
        { start: 30, end: 40, label: "31 - 40  高", color: "#e64546" },
        { start: 21, end: 30, label: "21 - 30  中", color: "#f57567" },
        { start: 11, end: 20, label: "11 - 20  低", color: "#ff9985" },
        { start: 0, end: 10, label: "0 -10 无数据", color: "#ffe5db" },
      ],
    }, */
        // 加载数据
        series: [],
      };

      // 监听图标容器大小，并改变图标大小
      window.addEventListener("resize", mapChart.resize);

      mapOption.series.push({
        name: "访问次数",
        type: "map",
        geoIndex: 0,
        label: {
          normal: {
            formatter: "{b}: {c}",
            position: "right",
            show: true,
          },
        },
        itemStyle: {
          // 图形样式
          normal: { label: { show: true } }, // 默认状态下地图的文字
          emphasis: { label: { show: true } }, // 鼠标放到地图上面显示文字
        },
        data: mapData,
      });
      mapChart.setOption(mapOption);
    });
  });
})(jQuery);

// 获取cpu使用率容器元素
var cpuChart = document.getElementById("cpu_memory_usage");

// 获取cpu负载容器元素
var cpuLoadChart = document.getElementById("cpu_avg_usage");

// 获取网络下载容器元素
var networkChart = document.getElementById("network_speed");

// 初始化cpu使用率折线图
var myChart = echarts.init(cpuChart, "dark", {
  renderer: "canvas",
  useDirtyRect: false,
});

// 初始化cpu负载折线图
var cpuLoadAvgChart = echarts.init(cpuLoadChart, "dark", {
  renderer: "canvas",
  useDirtyRect: false,
});

// 初始化下载网络折线图
var netChart = echarts.init(networkChart, "dark", {
  renderer: "canvas",
  useDirtyRect: false,
});

myChart.group = "group1";
cpuLoadAvgChart.group = "group1";
echarts.connect("group1");

// 定义cpu内存折线图配置项
var option = {
  title: {
    text: "cpu/内存资源监控图",
  },
  tooltip: {
    show: true,
    trigger: "axis",
    axisPointer: {
      type: "cross",
      label: {
        backgroundColor: "#6a7985",
      },
    },
    valueFormatter: (value) => value.toFixed(2) + "%",
  },
  legend: {
    data: ["CPU占用率", "内存占用率"],
  },
  grid: {
    left: "3%",
    right: "4%",
    bottom: "3%",
    containLabel: true,
  },
  toolbox: {
    feature: {
      saveAsImage: {},
      magicType: {
        show: true,
        type: ["line", "bar", "stack"],
      },
    },
  },
  xAxis: {
    type: "category",
    boundaryGap: false,
    data: [],
  },
  yAxis: {
    type: "value",
  },
  dataZoom: [
    {
      show: true,
      type: "slider",
      xAxisIndex: [0],
      start: 80,
      end: 100,
      backgroundColor: "transparent",
    },
    {
      show: true,
      type: "inside",
      xAxisIndex: [0],
      start: 80,
      end: 100,
    },
  ],
  series: [
    {
      name: "CPU占用率",
      data: [],
      type: "line",
      stack: "x",
      areaStyle: {},
      smooth: true,
      markPoint: true, //标记极值
      label: {
        show: false,
        position: "top",
        formatter: function (params) {
          return params.value;
        },
        textStyle: {
          fontSize: 12,
          fontWeight: "gray",
        },
      },
      emphasis: {
        scale: true,
        focus: "series",
        itemStyle: {
          normal: {
            show: false,
          },
        },
        label: {
          show: true,
        },
      },
    },
    {
      name: "内存占用率",
      data: [],
      type: "line",
      stack: "x",
      areaStyle: {},
      smooth: true,
      markPoint: true, //标记极值
      label: {
        show: false,
        position: "top",
        formatter: function (params) {
          return params.value;
        },
        textStyle: {
          fontSize: 12,
          fontWeight: "gray",
        },
      },
      emphasis: {
        scale: true,
        focus: "series",
        itemStyle: {
          normal: {
            show: false,
          },
        },
        label: {
          show: true,
        },
      },
    },
  ],
};

// 定义cpu负载折线图配置项
var cpuLoadAvgOption = {
  title: {
    text: "CPU负载使用率",
  },
  tooltip: {
    show: true,
    trigger: "axis",
    axisPointer: {
      type: "cross",
      label: {
        backgroundColor: "#6a7985",
      },
    },
    valueFormatter: (value) => value.toFixed(2) + "%",
  },
  legend: {
    data: ["1分钟负载", "5分钟负载", "15分钟负载"],
  },
  grid: {
    left: "3%",
    right: "4%",
    bottom: "3%",
    containLabel: true,
  },
  toolbox: {
    feature: {
      saveAsImage: {},
      magicType: {
        show: true,
        type: ["line", "bar", "stack"],
      },
    },
  },
  xAxis: {
    type: "category",
    boundaryGap: false,
    data: [],
  },
  yAxis: {
    type: "value",
  },
  dataZoom: [
    {
      show: true,
      type: "slider",
      xAxisIndex: [0],
      start: 80,
      end: 100,
      backgroundColor: "transparent",
    },
    {
      show: true,
      type: "inside",
      xAxisIndex: [0],
      start: 80,
      end: 100,
    },
  ],
  series: [
    {
      name: "1分钟负载",
      data: [],
      type: "line",
      stack: "x",
      areaStyle: {},
      smooth: true,
      markPoint: true, //标记极值
      label: {
        show: false,
        position: "top",
        formatter: function (params) {
          return params.value;
        },
        textStyle: {
          fontSize: 12,
          fontWeight: "gray",
        },
      },
      emphasis: {
        scale: true,
        focus: "series",
        itemStyle: {
          normal: {
            show: false,
          },
        },
        label: {
          show: true,
        },
      },
    },
    {
      name: "5分钟负载",
      data: [],
      type: "line",
      stack: "x",
      areaStyle: {},
      smooth: true,
      markPoint: true, //标记极值
      label: {
        show: false,
        position: "top",
        formatter: function (params) {
          return params.value;
        },
        textStyle: {
          fontSize: 12,
          fontWeight: "gray",
        },
      },
      emphasis: {
        scale: true,
        focus: "series",
        itemStyle: {
          normal: {
            show: false,
          },
        },
        label: {
          show: true,
        },
      },
    },
    {
      name: "15分钟负载",
      data: [],
      type: "line",
      stack: "x",
      areaStyle: {},
      smooth: true,
      markPoint: true, //标记极值
      label: {
        show: false,
        position: "top",
        formatter: function (params) {
          return params.value;
        },
        textStyle: {
          fontSize: 12,
          fontWeight: "gray",
        },
      },
      emphasis: {
        scale: true,
        focus: "series",
        itemStyle: {
          normal: {
            show: false,
          },
        },
        label: {
          show: true,
        },
      },
    },
  ],
};

// 定义网络折线图配置项
var netOption = {
  title: {
    text: "网络资源监控图",
  },
  tooltip: {
    show: true,
    trigger: "axis",
    axisPointer: {
      type: "cross",
      label: {
        backgroundColor: "#6a7985",
      },
    },
    valueFormatter: function (value) {
      if (value > 1000) {
        return (value / 1000).toFixed(1) + " MB/s";
      } else {
        return value + " KB/s";
      }
    },
  },
  legend: {
    data: [],
  },
  grid: [
    { left: "3%", top: "15%", bottom: "8%", width: "45%" },
    { right: "3%", top: "15%", bottom: "8%", width: "45%" },
  ],
  toolbox: {
    feature: {
      saveAsImage: {},
      magicType: {
        show: true,
        type: ["line", "bar", "stack"],
      },
    },
  },
  xAxis: [
    {
      type: "category",
      boundaryGap: false,
      gridIndex: 0,
      data: [],
    },
    {
      type: "category",
      boundaryGap: false,
      gridIndex: 1,
      data: [],
    },
  ],
  yAxis: [
    {
      name: "",
      type: "value",
      gridIndex: 0,
    },
    {
      name: "",
      type: "value",
      gridIndex: 1,
    },
  ],
  dataZoom: [
    {
      show: true,
      type: "slider",
      xAxisIndex: [0],
      start: 80,
      end: 100,
    },
    {
      show: true,
      type: "inside",
      xAxisIndex: [0],
      start: 80,
      end: 100,
    },
    {
      show: true,
      type: "slider",
      xAxisIndex: [1],
      start: 80,
      end: 100,
    },
    {
      show: true,
      type: "inside",
      xAxisIndex: [1],
      start: 80,
      end: 100,
    },
  ],
  series: [],
};

if (option && typeof option === "object") {
  myChart.setOption(option);
}

if (cpuLoadAvgOption && typeof cpuLoadAvgOption === "object") {
  cpuLoadAvgChart.setOption(cpuLoadAvgOption);
}

if (netOption && typeof netOption === "object") {
  netChart.setOption(netOption);
}

// 监听图标容器大小，并改变图标大小
window.addEventListener("resize", myChart.resize);

// 监听图标容器大小，并改变图标大小
window.addEventListener("resize", cpuLoadAvgChart.resize);

// 监听图标容器大小，并改变图标大小
window.addEventListener("resize", netChart.resize);

//格式化当前时间
function formatCurrentDate() {
  var date = new Date();
  var formattedDate = date.toLocaleString("default", {
    year: "numeric",
    month: "numeric",
    day: "numeric",
    hour: "numeric",
    minute: "numeric",
    second: "numeric",
  });
  return formattedDate;
}

// 定义全局资源使用率
var usages_data;

// 更新数据
function getData() {
  // 使用网络请求库访问后台接口，获取CPU的资源使用率
  axios.get("/api/v1.0/resources/usages").then(function (response) {
    usages_data = response.data;

    // 更新cpu、内存资源使用率图表时间(x轴显示的时间)
    option.xAxis.data.push(formatCurrentDate());

    // 更新cpu、内存资源使用率图表数据
    option.series[0].data.push(usages_data.cpu.percent);
    // 更新内存资源使用率图表数据
    option.series[1].data.push(usages_data.memory.percent);

    // 更新cpu负载使用率图表时间(x轴显示的时间)
    cpuLoadAvgOption.xAxis.data.push(formatCurrentDate());

    // 更新cpu负载使用率图表数据(y轴显示的数据 1分钟负载)
    cpuLoadAvgOption.series[0].data.push(parseFloat(usages_data.cpu.load_avg.split(", ")[0]));
    // 更新cpu负载使用率图表数据(y轴显示的数据 10分钟负载)
    cpuLoadAvgOption.series[1].data.push(parseFloat(usages_data.cpu.load_avg.split(", ")[1]));
    // 更新cpu负载使用率图表数据(y轴显示的数据 15分钟负载)
    cpuLoadAvgOption.series[2].data.push(parseFloat(usages_data.cpu.load_avg.split(", ")[2]));

    // 将数据渲染到图表
    myChart.setOption(option);

    // 将数据渲染到图表
    cpuLoadAvgChart.setOption(cpuLoadAvgOption);
  });
}

// 更新cpu、mem、cpu负载的页面展示
function setCpuMemCpuavgValue(data) {
  var cpu_element = document.getElementById("cpu-rate-percent");
  var mem_element = document.getElementById("mem-rate-percent");
  var cpu_avg_element = document.getElementById("cpu-load-avg");
  var cpu_avg_format =
    "1分钟: " +
    data.cpu.load_avg.split(", ")[0] +
    ", 5分钟: " +
    data.cpu.load_avg.split(", ")[1] +
    ", 15分钟: " +
    data.cpu.load_avg.split(", ")[2];
  cpu_element.innerHTML = data.cpu.percent + "%";
  mem_element.innerHTML = "总内存: " + data.memory.total + "GB, 已使用: " + data.memory.percent + "%";
  cpu_avg_element.innerHTML = cpu_avg_format;
}

// 更新数据
function getNetworkData() {
  // 使用网络请求库访问后台接口，获取CPU的资源使用率
  axios.get("/api/v1.0/resources/network_speed").then(function (response) {
    var data = response.data;
    netOption.xAxis[0].data.push(formatCurrentDate());
    netOption.xAxis[1].data.push(formatCurrentDate());
    if (netOption.series.length == 0) {
      for (var n = 0; n < data.length; n++) {
        netOption.legend.data.push(data[n].name);
        netOption.series.push({
          name: data[n].name,
          data: [data[n].rx_rate],
          type: "line",
          xAxisIndex: 0,
          yAxisIndex: 0,
          areaStyle: {},
          smooth: true,
          markPoint: true, //标记极值
          label: {
            show: false,
            position: "top",
            formatter: function (params) {
              return params.value;
            },
            textStyle: {
              fontSize: 12,
              fontWeight: "gray",
            },
          },
          emphasis: {
            scale: true,
            focus: "series",
            itemStyle: {
              normal: {
                show: false,
              },
            },
            label: {
              show: true,
            },
          },
        });
        netOption.series.push({
          name: data[n].name,
          data: [data[n].tx_rate],
          type: "line",
          xAxisIndex: 1,
          yAxisIndex: 1,
          areaStyle: {},
          smooth: true,
          markPoint: true, //标记极值
          label: {
            show: false,
            position: "top",
            formatter: function (params) {
              return params.value;
            },
            textStyle: {
              fontSize: 12,
              fontWeight: "gray",
            },
          },
          emphasis: {
            scale: true,
            focus: "series",
            itemStyle: {
              normal: {
                show: false,
              },
            },
            label: {
              show: true,
            },
          },
        });
      }

      netChart.setOption(netOption);
    }

    // 更新series.data数据
    for (var i = 0; i < netOption.series.length; i++) {
      for (var n = 0; n < data.length; n++) {
        if (data[n].name == netOption.series[i].name) {
          if (netOption.series[i].xAxisIndex == 0) {
            netOption.series[i].data.push(data[n].rx_rate); // push最新的data数据
          } else {
            netOption.series[i].data.push(data[n].tx_rate); // push最新的data数据
          }
        }
      }
    }
    netChart.setOption(netOption);
  });
}

// 定义变量 timer 用于保存 setInterval 的返回值
var timer;

// 开启 setInterval 的函数
function startInterval() {
  timer = setInterval(function () {
    getData();
    getNetworkData();
    setCpuMemCpuavgValue(usages_data);
  }, 5000); // 每隔 5 秒执行一次
}

// 关闭 setInterval 的函数
function stopInterval() {
  clearInterval(timer); // 停止 setInterval 的执行
}

document.getElementById("open_usage_monitor").addEventListener("click", function () {
  if (!timer) {
    startInterval();
    this.style.display = "none";
    var usage_close_btn = document.getElementById("close_usage_monitor");
    usage_close_btn.style.display = "block";
  } else {
    console.log("已经开启了实时监控服务");
  }
});

document.getElementById("close_usage_monitor").addEventListener("click", function () {
  if (timer) {
    stopInterval();
    this.style.display = "none";
    var usage_open_btn = document.getElementById("open_usage_monitor");
    usage_open_btn.style.display = "block";
    timer = null;
  } else {
    console.log("实时监控服务没有开启, 无法关闭");
  }
});
