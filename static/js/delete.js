document.addEventListener("DOMContentLoaded", function () {
  const delete_post_buttons = document.querySelectorAll(".delete-post-button");

  const modal = document.getElementById("modal");

  delete_post_buttons.forEach(function (button) {
    button.addEventListener("click", function (event) {
      event.preventDefault();
      modal.style.display = "flex";

      const deletionForm = document.getElementById("dashboard-form");
      const form_disclaimer = document.getElementById("form-disclaimer");
      const form_message = document.getElementById("form-message");
      const decline = document.getElementById("decline");
      const proceed = document.getElementById("proceed");

      form_disclaimer.innerHTML = "Do you really want to delete the post?";
      form_message.innerHTML = "Remember, there is no way back!";
      proceed.value = "Delete";

      proceed.className = "";

      decline.addEventListener("click", function (event) {
        event.preventDefault();
        modal.style.display = "none";
      });

      const postId = this.getAttribute("data-post-id");
      const csrfToken = this.getAttribute("data-csrf-token");
      const url = this.getAttribute("data-url");
      deletionForm.action = url;

      proceed.addEventListener("click", function (event) {
        event.preventDefault();
        fetch(deletionForm.action, {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": csrfToken,
          },
          body: "post_id=" + postId,
        })
          .then((response) => response.json())
          .then((data) => {
            console.log("Deleted: ", data);
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
