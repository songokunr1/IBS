var toggle = document.getElementById("menu-toggle")
var myNode = document.getElementById("wrapper");
var menuu = document.getElementById("place_for_menu");
var el = myNode.innerHTML
console.log(toggle)
toggle.onclick = () => {
  if (myNode.hasChildNodes()) {
  myNode.innerHTML = '';
  var toggle = document.getElementById("menu-toggle");}
  else {
  menuu.innerHTML = '';
  myNode.innerHTML = el;
  }
}



var alarms = document.querySelectorAll('.alert');
var i;
setTimeout(function(){
for (i = 0; i < alarms.length; i++) {
  alarms[i].remove();}
}, 3000);


