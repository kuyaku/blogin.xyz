document.addEventListener("DOMContentLoaded", function () {
  const unpublish_post_buttons = document.querySelectorAll(
    ".unpublish-post-button"
  );
  const modal = document.getElementById("modal");

  unpublish_post_buttons.forEach(function (button) {
    button.addEventListener("click", function (event) {
      event.preventDefault();
      modal.style.display = "flex";

      const unpublishForm = document.getElementById("dashboard-form");
      const form_disclaimer = document.getElementById("form-disclaimer");
      const form_message = document.getElementById("form-message");
      const decline = document.getElementById("decline");
      const proceed = document.getElementById("proceed");

      form_disclaimer.innerHTML = "Do you want to unpublish?";
      form_message.innerHTML =
        "All data (views, likes, comment) related to post will be deleted!";
      proceed.value = "Unpublish";

      proceed.className = "";

      decline.addEventListener("click", function (event) {
        event.preventDefault();
        modal.style.display = "none";
      });

      const postId = this.getAttribute("data-post-id");
      const csrfToken = this.getAttribute("data-csrf-token");

      proceed.addEventListener("click", function (event) {
        event.preventDefault();
        fetch(unpublishForm.action, {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": csrfToken,
          },
          body: "post_id=" + postId,
        })
          .then((response) => response.json())
          .then((data) => {
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
