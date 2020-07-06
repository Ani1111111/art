var A = document.getElementById("carticles");
var p = document.getElementById("cpoetry");
var sh = document.getElementById("cshayaries");
var s = document.getElementById("cstories");
var j = document.getElementById("cjokes");
var o = document.getElementById("cother");

var q = document.getElementById("query");
var sb = document.getElementById("sb");
A.addEventListener('click',function() {
    q.value = "carticles"; 
    sb.click();    
});

p.addEventListener('click',function() {
    q.value = "cpoetry"; 
    sb.click() 
});

sh.addEventListener('click',function() {
    q.value = "cshayaries"; 
    sb.click() 
});
s.addEventListener('click',function() {
    q.value = "cstories"; 
    sb.click() 
});
j.addEventListener('click',function() {
    q.value = "cjokes"; 
    sb.click() 
});
o.addEventListener('click',function() {
    q.value = "cother"; 
    sb.click() 
});
