document.addEventListener("DOMContentLoaded", function () {
  styleElement = document.getElementsByClassName("cke_inner");
  controlButton = document.getElementById("show-hide-styling");

  controlButton.addEventListener("click", function (event) {
    event.preventDefault();

    if (controlButton.innerHTML === "Show styling") {
      styleElement.style.display = "none";
      controlButton.innerHTML = "Hide styling";
    } else {
      styleElement.style.display = "block";
      controlButton.innerHTML = "Show styling";
    }
  });
});
