document.addEventListener("DOMContentLoaded", function () {
  const follow_forms = document.querySelectorAll(".follow-form");
  follow_forms.forEach((form) => {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          const followButton = form.querySelector(
            "button[name='follow-button']"
          );

          const bloggerId = this.getAttribute("data-blogger-id");
          const followerCountSpan = document.getElementById(
            "follower-count-" + bloggerId
          );
          const followerCount = parseInt(followerCountSpan.innerHTML);

          if (data.follow) {
            followButton.innerHTML = '<p id="unfollow">Unfollow</p>';
            followerCountSpan.innerHTML = followerCount + 1;
          } else {
            followButton.innerHTML = '<p id="follow">Follow</p>';
            followerCountSpan.innerHTML = followerCount - 1;
          }
        })
        .catch((error) => console.error("Error", error));
    });
  });
});
