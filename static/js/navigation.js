document.addEventListener("DOMContentLoaded", function () {
  navigationButton = document.getElementById("navigation-button");
  navigationButton2 = document.getElementById("username-header");
  navigationButton.addEventListener("click", function (event) {
    navItemsContainer = document.getElementById("header-nav-items");
    if (navItemsContainer.style.display === "flex") {
      navItemsContainer.style.display = "none";
    } else {
      navItemsContainer.style.display = "flex";
    }
  });

  navigationButton2.addEventListener("click", function (event) {
    navItemsContainer2 = document.getElementById("header-nav-items2");
    if (navItemsContainer2.style.display === "flex") {
      navItemsContainer2.style.display = "none";
    } else {
      navItemsContainer2.style.display = "flex";
    }
  });
});
