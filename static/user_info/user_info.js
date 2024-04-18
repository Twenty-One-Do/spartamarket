function getCsrfToken() {
  return document
    .querySelector('meta[name="csrf-token"]')
    .getAttribute("content");
}

document.addEventListener("DOMContentLoaded", function () {
  const imgElement = document.getElementById("img_btn");
  imgElement.addEventListener("click", function () {
    document.getElementById("file-input").click();
  });
});

document
  .getElementById("file-input")
  .addEventListener("change", function (event) {
    const file = event.target.files[0];
    if (file) {
      const formData = new FormData();
      formData.append("image", file);

      fetch(".", {
        method: "POST",
        headers: {
          "X-CSRFToken": getCsrfToken(),
        },
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          img_tag = document.getElementById("profile_img_a");
          img_tag.src = data["img_link"];
          img_tag = document.getElementById("profile_img_b");
          img_tag.src = data["img_link"];
        })
        .catch((error) => {});
    }
  });
