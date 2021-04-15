const DELAY = 12 * 1000;

let danmujs = null;
let ws = null;
let container = document.getElementsByClassName("danmu-row");
let len = container.length;

let count = 0;

window.onload = () => {
  registerWs();
  initDanmu();
  danmujs.start();
  // test();
};

function recvMsg(content) {
  danmujs.sendComment({
    // moveV: 50,
    id: Date.now(),
    duration: DELAY,
    txt: content,
    style: {
      color: "rgb(250, 250, 250)",
      // color: "#342E44",
      fontSize: '36px'
    },
    noDiscard: true,
  });
  return;
}

function registerWs() {
  ws = new WebSocket(`ws://danmu.deanti.wang/ws`);
  // ws = new WebSocket(`ws://127.0.0.1:9988/ws`);

  ws.open = (evt) => {
    ws.send("test");
    console.log("onOpen", evt)
  };
  ws.onmessage = (evt) => {
    console.log("onMessage", evt);
    recvMsg(evt.data)
  }
  ws.onerror = (evt) => {
    console.error("ws error", evt);
  },
  ws.onclose = (evt) => {
    console.warn("onClose", evt);
  }
}

function initDanmu() {
  danmujs = new DanmuJs({
    container: document.getElementById('container'),
    containerStyle: {
      zIndex: 100
    },
    area: {  //弹幕显示区域
      start: 0, //区域顶部到播放器顶部所占播放器高度的比例
      end: 1 //区域底部到播放器顶部所占播放器高度的比例
    },
    live: true,
    bOffset: 20,
    channelSize: 70, // 轨道大小
    mouseControl: false, // 打开鼠标控制, 打开后可监听到 bullet_hover 事件。danmu.on('bullet_hover', function (data) {})
    mouseControlPause: false
  });
}

function test() {
  const delay = Math.random() * 3 + 0.02;
  setTimeout(() => {
    recvMsg("deantiwang: test");
    test();
  }, delay * 1000);
}