document.addEventListener("DOMContentLoaded", function () {
  const IMG_LIKED = "heart.png";
  const IMG_NOTLIKED = "heart2.png";
  const likeForm = document.getElementById("like-form");

  if (likeForm) {
    likeForm.addEventListener("submit", function (event) {
      event.preventDefault(); // prevent the default form submission
      fetch(likeForm.action, {
        method: "POST",
        body: new FormData(likeForm),
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          const likeButton = likeForm.querySelector(
            "button[name='like-button']"
          );
          likeButton.innerHTML = data.liked
            ? `<img class="liked-img" src="../../static/images/icons/${IMG_LIKED}">`
            : `<img class="liked-img" src="../../static/images/icons/${IMG_NOTLIKED}">`; // with respect to the template
        })
        .catch((error) => console.error("Error: ", error));
    });
  }
});
