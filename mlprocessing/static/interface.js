window.addEventListener("DOMContentLoaded", (event) => {
  var cam1Btn = document.getElementById('cam1');
  var cam2Btn = document.getElementById('cam2');
  var cam3Btn = document.getElementById('cam3');
  var image = document.getElementById('image');
});
function changeText(newText) {
  // Get the HTML element by its ID
  var messageElement = document.getElementById('changedata');
  
  // Change the text of the HTML element
  messageElement.innerText = newText;
}
var index = 0

setInterval(function () {
  console.log("HI")
  document.getElementById("c"+index).className = "carousel-item"
  index = (index + 1) % 4
  document.getElementById("c"+index).className = "carousel-item active"
}, 1000);