function welcome(){
    alert("Hello there welcome to mobimechanic")
}





var x = document.getElementById('menu-list')
function togglemenu(x){
    x = document.getElementById(x);
    if(x.style.display == 'none'){
        x.style.display = 'block';
    } else {
        x.style.display = 'none';
    }
}
