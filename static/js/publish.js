document.addEventListener("DOMContentLoaded", function () {
  const publish_post_buttons = document.querySelectorAll(
    ".publish-post-button"
  );

  const modal = document.getElementById("modal");

  publish_post_buttons.forEach(function (button) {
    button.addEventListener("click", function (event) {
      event.preventDefault();
      modal.style.display = "flex";

      const publishForm = document.getElementById("dashboard-form");
      const form_disclaimer = document.getElementById("form-disclaimer");
      const form_message = document.getElementById("form-message");
      const decline = document.getElementById("decline");
      const proceed = document.getElementById("proceed");

      form_disclaimer.innerHTML = "Do you really want to publish your post?";
      form_message.innerHTML =
        "Post will be published. Any user will be able to read, like & comment on your post!";
      proceed.value = "Publish";

      proceed.className = "post-publish-submit";

      decline.addEventListener("click", function (event) {
        event.preventDefault();
        modal.style.display = "none";
      });

      const postId = this.getAttribute("data-post-id");
      const csrfToken = this.getAttribute("data-csrf-token");
      const url = this.getAttribute("data-url");
      publishForm.action = url;
      proceed.addEventListener("click", function (event) {
        event.preventDefault();
        fetch(publishForm.action, {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": csrfToken,
          },
          body: "post_id=" + postId,
        })
          .then((response) => response.json())
          .then((data) => {
            console.log("Published: ", data);
            location.reload();
          })
          .catch((error) => {
            console.error("Error: ", error);
          });
        modal.style.display = "none";
      });
    });
  });
});
