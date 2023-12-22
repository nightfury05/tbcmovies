let searchInput = document.getElementById("searchInput")
let searchButton = document.getElementById("searchButton")

searchButton.addEventListener("click", () => {
    window.location.href = "/search/" + searchInput.value
})