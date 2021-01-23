const modal = document.getElementById("modal")

window.onclick = function(event) {
    if (event.target === modal)
        hideModal()
}

function hideModal() {
    document.getElementById("modal").style.display = "none"
}

function showModal(text, action) {
    document.getElementById("modal").style.display = "block"
    document.getElementById("modal-text").textContent = text
    document.getElementById("modal-ok-button").onclick = () => {
        action()
        hideModal()
    }
}