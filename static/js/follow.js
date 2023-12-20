document.addEventListener("DOMContentLoaded", function () {
  const followForm = document.getElementById("follow-form");

  if (followForm) {
    followForm.addEventListener("submit", function (event) {
      event.preventDefault(); // prevent the default form submission
      fetch(followForm.action, {
        method: "POST",
        body: new FormData(followForm),
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          const followButton = followForm.querySelector(
            "button[name='follow-button']"
          );
          const followerCountSpan = document.getElementById("follower-count");
          const followerCount = parseInt(followerCountSpan.innerHTML);

          if (data.follow) {
            followButton.innerHTML = '<p id="unfollow">UNFOLLOW</p>';
            followerCountSpan.innerHTML = followerCount + 1;
          } else {
            followButton.innerHTML = '<p id="follow">FOLLOW</p>';
            followerCountSpan.innerHTML = followerCount - 1;
          }
        })
        .catch((error) => console.error("Error: ", error));
    });
  }
});
