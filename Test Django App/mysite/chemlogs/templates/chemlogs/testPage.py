coll = document.getElementsByClassName("collapsible")
def func:
    this.classLast.toggle("active")
    content = this.nextElementSibling
    if content.style.display == "block":
        content.style.display = "none"
    else:
        content.style.display = "block"

for x in coll:
    coll[x].addEventListener("click", func())