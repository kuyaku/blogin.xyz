document.addEventListener("DOMContentLoaded", function () {
  let editor;

  const mainHeading = document.getElementById("id_title");
  const subHeading = document.getElementById("id_sub_title");
  const category = document.getElementById("id_category_names");
  const tagData = document.getElementById("id_tag_names");

  function saveContentToLocalStorage() {
    const content = editor.getData();
    localStorage.setItem("editorContent", content);
  }

  function handleButtonClick() {
    const stylePallete = editor.container["$"].querySelector("#cke_1_top");
    const styleButton = document.getElementById("show-hide-styling");

    if (styleButton.innerHTML === "Show styling") {
      stylePallete.style.display = "block";
      styleButton.innerHTML = "Hide styling";
    } else {
      stylePallete.style.display = "none";
      styleButton.innerHTML = "Show styling";
    }
  }

  function setHeadings() {
    let title = JSON.parse(localStorage.getItem("mainHeading"));
    let subTitle = JSON.parse(localStorage.getItem("subHeading"));
    let categories = JSON.parse(localStorage.getItem("category"));
    let tags = JSON.parse(localStorage.getItem("tagData"));

    if (title) {
      mainHeading.value = title;
    }

    if (subTitle) {
      subHeading.value = subTitle;
    }

    if (categories) {
      category.value = categories;
    }

    if (tags) {
      tagData.value = tags;
    }
  }

  function saveHeadingToStorage(heading, data) {
    localStorage.setItem(heading, JSON.stringify(data));
  }

  function initializeHeading() {
    let typingTimer;
    const doneTypingInterval = 500; // 1 second

    setHeadings();

    mainHeading.addEventListener("input", function () {
      clearTimeout(typingTimer);
      typingTimer = setTimeout(
        () => saveHeadingToStorage("mainHeading", mainHeading.value),
        doneTypingInterval
      );
    });
    subHeading.addEventListener("input", function () {
      clearTimeout(typingTimer);
      typingTimer = setTimeout(
        () => saveHeadingToStorage("subHeading", subHeading.value),
        doneTypingInterval
      );
    });
    category.addEventListener("input", function () {
      clearTimeout(typingTimer);
      typingTimer = setTimeout(
        () => saveHeadingToStorage("category", category.value),
        doneTypingInterval
      );
    });
    tagData.addEventListener("input", function () {
      clearTimeout(typingTimer);
      typingTimer = setTimeout(
        () => saveHeadingToStorage("tagData", tagData.value),
        doneTypingInterval
      );
    });
  }

  function initializeEditor() {
    editor = CKEDITOR.instances["stylingPallete"];

    if (!editor) {
      CKEDITOR.on("instanceReady", function (event) {
        editor = event.editor;

        // Load saved content from local storage on page load
        const savedContent = localStorage.getItem("editorContent");
        if (savedContent) {
          editor.setData(savedContent);
        }

        // Save content to local storage as the user stops typing
        let typingTimer;
        const doneTypingInterval = 1000; // 1 second

        editor.on("change", function () {
          clearTimeout(typingTimer);
          typingTimer = setTimeout(
            saveContentToLocalStorage,
            doneTypingInterval
          );
        });

        const styleButton = document.getElementById("show-hide-styling");
        styleButton.addEventListener("click", handleButtonClick);
      });
    }
  }

  initializeHeading();
  initializeEditor();

  // Remove event listeners when leaving the page
  window.addEventListener("beforeunload", function () {
    if (editor) {
      editor.removeListener("change", saveContentToLocalStorage);

      const styleButton = document.getElementById("show-hide-styling");
      styleButton.removeEventListener("click", handleButtonClick);
    }
  });
});
