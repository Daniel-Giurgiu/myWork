function deleteMe(id){
  fetch('http://127.0.0.1:5000/GET/' + id, {
      method: 'DELETE',
    })
    .then(res => {
      elem = document.getElementById(id)
      elem.remove();
    })
    .catch(err => console.log(err))
}

function addTable() {
  table = document.getElementsByTagName("table")
  console.log(table[0])
  var newtr = document.createElement('TR');
  table[0].appendChild(newtr);
    
  var id = document.createElement('TD');
  var photo = document.createElement('TD');
  var firstname = document.createElement('TD');
  var lastname = document.createElement('TD'); 
  var height = document.createElement('TD'); 
  var btn = document.createElement('button')


  tr = document.getElementsByTagName("tr")
  var totalRowCount = table[0].rows.length;
  console.log(totalRowCount-1)

  id.appendChild(document.createTextNode(totalRowCount-1));
  newtr.appendChild(id);

  ph = `<input type = "file" name ="file">`
  photo.innerHTML= ph;
  newtr.appendChild(photo);

  fn = `<input type = "text" name = "FirstName">`
  firstname.innerHTML= fn;
  newtr.appendChild(firstname);

  ln = `<input type = "text" name = "LastName">`
  lastname.innerHTML= ln;
  newtr.appendChild(lastname);

  hg = `<input type = "text" name = "height">`
  height.innerHTML= hg;
  newtr.appendChild(height);



  bt = `<button type = "button" name = "btn">Post</button>`
  btn.innerHTML= bt;
  newtr.appendChild(btn);
  btn.addEventListener("click", function(){postPers(photo, firstname, lastname, height, btn)})

}

function postPers(photo, firstname, lastname, height, btn){
  
  let postForm = new FormData();
  postForm.append("photo", photo.firstChild.files[0]);
  postForm.append("FirstName", firstname.firstChild.value);
  postForm.append("LastName", lastname.firstChild.value);
  postForm.append("height", height.firstChild.value);

  fetch("http://127.0.0.1:5000/add", {
    method: 'POST',
    body: postForm
  })
  .then(res => res.json())
  .then(data => {
    html = `<img src="/imag/small_`+ data["bigpath"] + `"></img>`;
    photo.innerHTML = html
    firstname.innerHTML = firstname.firstChild.value;
    lastname.innerHTML = lastname.firstChild.value;
    height.innerHTML = height.firstChild.value;
    btn.innerHTML =  `<button class="btn btn-outline-danger" onclick="deleteMe('{{ u.ID }}')" ><i class="fa-sharp fa-solid fa-trash"></i></button>`
  })
  .catch(err => {
    console.error(err);
  });
}





function update(oldValue, field, ID, newValue) {
  let html = 
  `<input id="input-${field}-${ID}" type="text" name="${field}" value="${newValue}">&nbsp
  <button id="cancel-${ID}">❌</button>&nbsp
  <button id="ok-${ID}">✅</button>`;
  oldValue.innerHTML = html;
  var ok = document.getElementById(`ok-${ID}`);
  var cancel = document.getElementById(`cancel-${ID}`);
  var inputElem = document.getElementById(`input-${field}-${ID}`);
  ok.addEventListener("click", function() { okClick(inputElem, oldValue, ID, field) });
  cancel.addEventListener("click", function() { cancelClick(oldValue, newValue) });
}
function okClick(input, oldValue, updatedID, field) {
  
  let updateForm = new FormData();
  updateForm.append(field, input.value);

  fetch("http://127.0.0.1:5000/update/"+ field +  '/' + updatedID, {
    method: 'PUT',
    body: updateForm
  })
  .then(res => {
    if(res.status == 200){
      var valueInput = input.value;
      oldValue.innerHTML = valueInput;
    }  
  })
  .catch(err => {
    console.error(err);
  });

}

function cancelClick(oldValue, newValue) {
  oldValue.innerHTML = newValue;
}