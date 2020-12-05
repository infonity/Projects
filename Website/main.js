window.onscroll = function() {startScroll()}

var navbar = document.getElementById("navbar");
var sticky = navbar.offsetTop;

function startScroll(){
    if (window.pageYOffset >= sticky){
        navbar.classList.add("sticky");
    }else{
        navbar.classList.remove("sticky");
    }
}