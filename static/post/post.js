like_num = document.getElementById("like_num");

function getCsrfToken() {
  return document
    .querySelector('meta[name="csrf-token"]')
    .getAttribute("content");
}

async function push_likes_btn(event) {
  var btn = event.target;
  var post_id = btn.getAttribute("post_id");
  btn.disabled = true;

  const response = await fetch("../../like/", {
    method: "POST",
    headers: {
      "content-Type": "application/json",
      "X-CSRFToken": getCsrfToken(),
    },
    body: JSON.stringify({ post_id: post_id }),
  });

  if (response.ok) {
    const result = await response.json();
    like_num.innerHTML = "찜수: " + result.new_like_num.toString() + " |";
    if (result.already_like) {
    } else {
    }
  }

  setTimeout(() => {
    btn.disabled = false;
  }, 500);

  return 0;
}
