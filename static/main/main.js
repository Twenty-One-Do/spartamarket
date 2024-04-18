let page = 1;
let no_more = false;
$(window).scroll(function () {
  if ($(window).scrollTop() + $(window).height() > $(document).height() - 100) {
    loadData();
    search_func();
  }
});

function loadData() {
  if (no_more) {
    return false;
  }
  let sort_by = $("#sort_by_q").attr("sort_by");
  page++;
  $.ajax({
    url: "/load_more/?sort_by=" + sort_by,
    data: { page: page },
    type: "GET",
    success: function (response) {
      let no_more_data = response.has_more != null;
      if (no_more_data) {
        no_more = true; // 서버로부터 더 이상 데이터가 없다는 응답을 받음
      } else {
        $("#post-div").append(response);
      }
    },
    error: function (error) {},
  });
}

regex = /^[0-9a-zA-Z가-힣]+$/;

function check_qual(value, min, max, regex) {
  return value.length >= min && value.length <= max && regex.test(value);
}

const search_inp = document.getElementById("search_inp");
const posts = document.getElementById("post-div").children;

async function search_func(event) {
  var search_query = search_inp.value; // this.value 대신 event.target.value 사용
  if (check_qual(search_query, 0, 20, regex) || search_query == "") {
    const response = await fetch("search/?search_query=" + search_query, {
      method: "GET",
      headers: { "content-Type": "application/json" },
    });
    var res_ids = [];
    if (response.ok) {
      const result = await response.json();
      res_ids = result.res_ids;
    }
    for (let post of posts) {
      let this_post_id = Number(post.getAttribute("id")); // let을 추가하여 변수를 명확히 선언
      if (res_ids.includes(this_post_id)) {
        post.style.display = "block";
      } else {
        post.style.display = "none";
      }
    }
  }
}

// 이벤트 리스너를 입력 요소에 추가
search_inp.addEventListener("input", search_func);
