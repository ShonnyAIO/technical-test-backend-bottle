const login = document.getElementById("form-login");
const buttonRegister = document.getElementById("register-button");

login.addEventListener("submit", (e) => {
  e.preventDefault();
  const username = login["user"].value;
  const password = login["password"].value;
  const data = {
    username: username,
    password: password
  };
  console.log(data);

  fetch("http://localhost:8000/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      localStorage.clear();
      localStorage.setItem("jwtToken", data.jwtToken);
      localStorage.setItem("refreshToken", data.refreshToken);
      if (data.jwtToken && data.refreshToken) {
        window.location.href = "/todos";
      }
    });
});

buttonRegister.addEventListener("click", () => {
  window.location.href = "/register";
});
