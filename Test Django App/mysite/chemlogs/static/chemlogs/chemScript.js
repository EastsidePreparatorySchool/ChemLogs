var coll = document.getElementsByClassName("content");

for (var i = 0; i < coll.length; i++) {
  // hide all collapsible content on page load
  hide(coll[i]);
}

// toggle visibility given ID
function toggleVisibilityId(id) {
  toggleVisibility(document.getElementById(id));
}

// toggle a collapsible between shown and hidden
function toggleVisibility(content) {
  if (content.style.maxHeight && content.style.maxHeight != "0px") {
    hide(content);
  } else {
    show(content);
  }
}

// hide a collapsible
function hideId(id) {
  hide(document.getElementById(id));
}

function hide(content) {
  content.style.maxHeight = "0px";
}

// show a collapsible
function showId(id) {
  showId(document.getElementById(id));
}

function show(content) {
  content.style.maxHeight = content.scrollHeight + "px";
}

// Used on page load. Changes how the slider renders.
function modifySlider(max) {
    slider = document.getElementById("trSlide");
    slider.type = "range";
    slider.min = "0";
    slider.max = max;
    slider.value = "0";
    slider.style = "margin: 0vw;";
}

// maintain scroll position when reloading a page
function setScrollListener() {
  // from https://stackoverflow.com/questions/9377951/how-to-remember-scroll-position-and-scroll-back
  $(document).ready(function () {
    if (localStorage.getItem("chemlogs-quote-scroll") != null) {
        $(window).scrollTop(localStorage.getItem("chemlogs-quote-scroll"));
    }
    $(window).on("scroll", function() {
        localStorage.setItem("chemlogs-quote-scroll", $(window).scrollTop());
    });
  });
}

// override the autoscroll so that you'll reload at top of page
function scrollTopOnReload() {
  localStorage.setItem("chemlogs-quote-scroll", 0);
}