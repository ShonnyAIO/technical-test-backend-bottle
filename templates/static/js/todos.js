const todo = document.getElementById("form-note");
const container = document.getElementById("notes-container");
const jwt = localStorage.getItem("jwtToken");
const refreshToken = localStorage.getItem("refreshToken");

const showNotes = (data) => {
  if (!data && !data[0].length && !data[1].length) {
    return (container.innerHTML = `<h2>No hay tareas que mostrar</h2>`);
  }
 
  container.innerHTML = `<br>`
 
  for (const todo of data) {
    if(todo){
      console.log(todo);
      container.innerHTML += `<div class="note">
            <h3>${todo.titulo}</h3>
            <p>
              ${todo.descripcion}
            </p>
          </div>`;
    }

  }
   container.innerHTML += `<h2>Lista de actividades</h2>`;
};

const request = () => {
  fetch("http://localhost:8000/api/all", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "jwtToken": jwt,
      "refreshToken": refreshToken,
    },
  }).then(response => response.json())
    .then(res => {
      console.log(res)
      showNotes(res.data)
    }).catch((err)=>{
      showNotes()
    })
    
};

// Envia las tareas
todo.addEventListener("submit", (e) => { e.preventDefault();
  const titulo = todo["titulo"].value;
  const descripcion = todo["descripcion"].value;

  const data = {
    titulo,
    descripcion,
  };

  

  fetch("http://localhost:8000/api/create", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "jwtToken": jwt,
      "refreshToken": refreshToken,
    },
    body: JSON.stringify(data),
  }).then((response) => {
    if (response.status == 201) {
      request();
    }
    todo.reset()

  });
});

window.addEventListener("load", () => {
  request();
});
