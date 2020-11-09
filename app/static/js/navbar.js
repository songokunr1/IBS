//$("#menu-toggle").click(function(e) {
//  e.preventDefault();
//  $("#wrapper").toggleClass("toggled");
//alert("Hello! I am an alert box!!");   background-color: #2574A9;
const toggle = document.getElementById("menu-toggle")
const myNode = document.getElementById("wrapper");
const el = myNode.innerHTML
console.log(toggle)
toggle.onclick = () => {
  if (myNode.hasChildNodes()) {
  myNode.innerHTML = '';}
  else {
  myNode.innerHTML = el;
  }
}