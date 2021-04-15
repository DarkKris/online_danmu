
const nameSetterBox = document.getElementsByClassName("name-setter")[0];
const tooltipsBox = document.getElementsByClassName("tooltips")[0];
const danmuBox = document.getElementById("danmu-input");

const NICK_KEY = "danmu-user-name";

let userNick = "";

window.onload = () => {
  const nick = localStorage.getItem(NICK_KEY);
  if (nick !== null) {
    // 输入过昵称了
    nameSetterBox.parentElement.removeChild(nameSetterBox);
    userNick = nick;
    document.getElementById("js-nick").innerText = nick;
  }
}

// 设置昵称
function setName() {
  const input = document.getElementById("nick-input");
  const nick = input.value;
  if (!!nick) {
    userNick = nick;
    localStorage.setItem(NICK_KEY, nick);
    nameSetterBox.parentElement.removeChild(nameSetterBox);
    document.getElementById("js-nick").innerText = nick;
  } else {
    alert("不能输入空字符串");
  }
}

function send() {
  const content = danmuBox.value;
  fetch("http://danmu.deanti.wang/api", {
    method: "POST",
    accept: "application/json",
    "content-type": "application/json",
    body: JSON.stringify({
      content: userNick + ": " + content
    })
  }).then((resp) => {
    if (resp.ok) {
      // send OK
      danmuBox.value = "";
      show("发送成功！");
    } else {
      show("发送失败");
      console.error(resp);
    }
  });
}

/* TOOLTIPS */

let tooltipsTimeout = null;

function show(message) {
  tooltipsBox.innerHTML = message;
  tooltipsBox.classList.add("active");
  tooltipsTimeout = setTimeout(() => {
    hidden()
  }, 3000);
}

function hidden() {
  clearTimeout(tooltipsTimeout);
  if (tooltipsBox.className.includes("active")) {
    tooltipsBox.classList.remove("active");
  }
}