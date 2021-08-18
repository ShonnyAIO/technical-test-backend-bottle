const register = document.getElementById("form-register")

register.addEventListener("submit", (e) => {
  e.preventDefault();
  const username = register["user"].value;
  const password = register["password"].value;

  const dataRegister = {
    username:username,
    password: password,
  };
  console.log(dataRegister);

  fetch("http://127.0.0.1:8000/api/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(dataRegister),
  })
    .then(response => {console.log(response)
      if(response.status === 201){
          window.location.href = '/';
      }
    } ).catch(err=>console.log(err))
    

});
