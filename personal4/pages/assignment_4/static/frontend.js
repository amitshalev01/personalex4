function frontendFunction() {
    var frontend_form = document.getElementById("from_frontend");
    var idInput = frontend_form.elements[0].value
    let element = document.createElement('a');
    element.href = 'https://reqres.in/api/users';
    element.pathname = element.pathname + '/' + idInput;
    fetch(element.href).then(
        response => response.json()
    ).then(
        responseOBJECT => createUsersList(responseOBJECT.data)
    ).catch(
        err => console.log(err)
    );
}



function createUsersList(response){
    const currMain = document.querySelector("main")
    const section = document.createElement('section')
    section.innerHTML = `
            <div class="polaroid" style="background-color: white; width: 80%;margin-bottom: 25px; margin-left: 10%;   box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);">
            <img style=" width:100%" src="${response.avatar}" alt="Profile Picture"/>
             <div class="container" style="padding: 10px 20px; " >
            <h4> ${response.first_name} ${response.last_name}</h4>
                <h6> email: ${response.email} </h6>
               <a href="mailto:${response.email}">Send Email</a>
              </div>
            </div>
        `
        currMain.appendChild(section)
        currMain.replaceChild(section, currMain.childNodes[0]);
}
