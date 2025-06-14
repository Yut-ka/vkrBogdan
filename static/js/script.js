const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});


jQuery("#search-icon").click(function() {
  jQuery(".nav").toggleClass("search");
  jQuery(".nav").toggleClass("no-search");
  jQuery(".search-input").toggleClass("search-active");
});

jQuery('.menu-toggle').click(function(){
   jQuery(".nav").toggleClass("mobile-nav");
   jQuery(this).toggleClass("is-active");
});



document.addEventListener('DOMContentLoaded', function () {
  // Вход
  document.querySelector('.sign-in-form').addEventListener('submit', function (e) {
    e.preventDefault();
    let form = e.target;
    let data = new FormData(form);
    let errorDiv = form.querySelector('.ajax-error');
    errorDiv.style.display = "none";
    fetch('/ajax_login', {
      method: 'POST',
      body: data,
    })
    .then(response => response.json())
    .then(res => {
      if (res.success) {
        window.location.href = "/main/";
      } else {
        errorDiv.textContent = res.message;
        errorDiv.style.display = "";
      }
    });
  });

  // Регистрация
  document.querySelector('.sign-up-form').addEventListener('submit', function (e) {
    e.preventDefault();
    let form = e.target;
    let data = new FormData(form);
    let errorDiv = form.querySelector('.ajax-error');
    errorDiv.style.display = "none";
    fetch('/ajax_register', {
      method: 'POST',
      body: data,
    })
    .then(response => response.json())
    .then(res => {
      if (res.success) {
        window.location.href = "/main/";
      } else {
        errorDiv.textContent = res.message;
        errorDiv.style.display = "";
      }
    });
  });
});