var toggle = document.getElementById("menu-toggle")
var myNode = document.getElementById("wrapper");
var el = myNode.innerHTML
console.log(toggle)
toggle.onclick = () => {
  if (myNode.hasChildNodes()) {
  myNode.innerHTML = '';}
  else {
  myNode.innerHTML = el;
  }
}



var alarms = document.querySelectorAll('.alert');
var i;
setTimeout(function(){
for (i = 0; i < alarms.length; i++) {
  alarms[i].remove();}
}, 3000);


