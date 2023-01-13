var coll = document.getElementsByClassName("collapsible");
        var i;

        for (i = 0; i < coll.length; i++) {
          coll[i].addEventListener("click", function() {
            this.classList.toggle("active");
            var content = this.nextElementSibling;
            if (content.style.display === "none") {
              content.style.display = "block";
            } else {
              content.style.display = "none";
            }
          });
        }
        
        var aD = document.getElementById("addDropdown")

        function down() {
            aD = document.getElementById("addDropdown")
            
            if (aD.innerHTML == "&#9650;") {
                aD.innerHTML = "&#9660;"
            } else {
                aD.innerHTML = "&#9650;"
            }
        }

        // Used on page load. Changes how the slider renders.
        function modifySlider() {
            slider = document.getElementById("trSlide");
            slider.type = "range";
            slider.min = "0";
            slider.max = "100";
            slider.value = "0";
        }

        // Used when "remove" is clicked. Makes slider value negative. Hopefully does not affect frontend.
        function negateSliderValue() {
            slider = document.getElementById("trSlide");
            slider.min = -100; // this is not a great solution to the problem that value can't be less than min
            slider.value = -slider.value;
        }

        var notif = document.getElementById("notif")

        function notif() {
            notif 
        }