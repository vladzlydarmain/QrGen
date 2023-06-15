let wrapper = document.querySelector(".wrapper-end")
let button = document.querySelector(".end-subscribe")

function lightDown(){
    wrapper.style = "opacity: 1; z-index: 4"

}

function lightUp(){
    wrapper.style = "opacity: 0; z-index: -1;"
}

button.addEventListener("hover", lightDown)
wrapper.addEventListener("unhover", lightUp)