
var btn = document.querySelector('.mouse-cursor-gradient-tracking')

btn.onmousemove = function(e)
{
  var x = e.pageX - btn.offsetLeft - btn.offsetParent.offsetLeft
  var y = e.pageY - btn.offsetTop - btn.offsetParent.offsetTop
  btn.style.setProperty('--x', x + 'px')
  btn.style.setProperty('--y', y + 'px')
}

function previewFile() {
    var preview = document.getElementById("blah");
    var file    = document.querySelector('input[type=file]').files[0];
    var reader  = new FileReader();

    reader.addEventListener("load", function () {
        preview.src = reader.result;
    }, false);

    if (file) {
        reader.readAsDataURL(file);
    }
  }

function colour_randomiser(css_string) {
  var colors = ['#90d1df', '#f4d30f', '#fd9900', '#805DA1', '#25876c'];
  var random_color = colors[Math.floor(Math.random() * colors.length)];
  $(css_string).css('background-color', random_color);
}

function navbar_button() {
  $(document).ready(function(){
    $(".purpleButton").click(function(){
      $("nav").slideToggle(500);
      $("icons").slideToggle(500);
    })
  })
}
