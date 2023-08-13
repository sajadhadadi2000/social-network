

function editForm(id){
    const form = document.querySelector("#editpost");
    if (form.style.display === 'block'){
        form.style.display = 'none';
    } else {
        form.style.display = 'block';
        fetch(`/edit/${parseInt(id)}`)
        .then(response => response.json())
        .then(post =>{
            document.querySelector("#post-id").value = post.id
            document.querySelector("#post-title").value = post.title
            document.querySelector("#post-body").value = post.body
        })
        window.scrollTo({
            top: 0,
            left: 0,
            behavior: "smooth",
          });
    }
}

function editPost(){
    const id = document.querySelector("#post-id").value
    fetch(`/edit/${id}`, {
        method: 'POST',
        body: JSON.stringify({
            id: id,
            title: document.querySelector("#post-title").value,
            body: document.querySelector("#post-body").value
        })
      })
      .then(response => response.json())
      .then(result => {
          // Print result
          console.log(result);
      });
}

function follow(){
  const following = document.querySelector("#follow");
  const nfollower = document.querySelector("#nfollower");
  
  fetch(`/follow/${parseInt(following.dataset.user)}`)
  .then(response => response.json())
  .then(data => {
    following.innerHTML = data.button
    nfollower.innerHTML = data.nfollower
    console.log("ok")
    });
}

async function like(id){
    await fetch("/like",{
        method: 'PUT',
        body: JSON.stringify({
            id: id
        })
    })
    .then(response=> response.json())
    .then(result=>{
        document.getElementById(`${id.toString()}`).innerHTML = `${result.like}`
        const buttonlike = document.getElementById(`buttonlike${id}`)
        if(result.buttonlike){
            buttonlike.className = "w-25 btn btn-outline-secondary"
            buttonlike.innerHTML = "Unlike"
        } else {
            buttonlike.className = "w-25 btn btn-outline-danger"
            buttonlike.innerHTML = "Like"
        }
    })
}

