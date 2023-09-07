var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    // if (content.style.display === "none") {
    //   content.style.display = "block";
    // } else {
    //   content.style.display = "none";
    // }
    if (content.style.maxHeight && content.style.maxHeight != "0px"){
      content.style.maxHeight = "0px";
      //content.style.visibility = "collapse";
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
      //content.style.visibility = "visible";
    }
  });
}

// hide a collapsible. not used
function hide(content) {
  content.style.maxHeight = "0px";
}

// hide one very specific collapsible. not used
function hideChemDeleteForm() {
  hide(document.getElementById("chemDeleteForm"))
  alert("hidden")
}

// Used on page load. Changes how the slider renders.
function modifySlider(max) {
    slider = document.getElementById("trSlide");
    slider.type = "range";
    slider.min = "0";
    slider.max = max;
    slider.value = "0";
    slider.style = "margin: 0vw;"
}

// Used when "remove" is clicked. Makes slider value negative. Hopefully does not affect frontend.
/*function negateSliderValue() {  i believe this is unused
    slider = document.getElementById("trSlide");
    slider.min = -100; // this is not a great solution to the problem that value can't be less than min
    slider.value = -slider.value;
}*/