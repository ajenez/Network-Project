document.addEventListener('DOMContentLoaded', function() {
    

    // Edit Posts
    document.querySelectorAll('.edit').forEach(btn => {
        btn.onclick = function () {
            btn.style.display = 'none'
            console.log(btn.dataset.postid)
            let contentDiv = document.querySelector(`#content${btn.dataset.postid}`)
            contentDiv.innerHTML = 
                `<form id="edit-post">
                    <div class="form_group">
                        <textarea required id="edit-post-text" style="resize:none;">${contentDiv.innerHTML.trim()}</textarea>
                    </div>
                    <input style="padding: 5px;" type="submit" class="btn btn-primary post-submit" value="Save"></input>
                </form>`;
        
            document.querySelector('#edit-post').onsubmit = () => {
                const content = document.querySelector('#edit-post-text').value;
                const post_id = btn.dataset.postid
                console.log(post_id)
                console.log(JSON.stringify({content,post_id}))
                console.log("working")
                
                fetch('/posting',{
                    method: 'PUT',
                    body: JSON.stringify({content,post_id})
                })
                    .then(response => response.json())
                    .then(result => {
                        console.log(result)
                        if (result.error) {
                            console.log(`Error with post: ${result.error}`);
                        } else{
                            console.log(result.message)
                            contentDiv.innerHTML = content
                            btn.style.display ='block'
                        }
                    })
                return false
            }
        }
    })


  //Like Posts 
  document.querySelectorAll('.add_like').forEach(btn => {
    btn.onclick = function () {
        const post_id = parseInt(document.querySelector(`#current_post${btn.dataset.postid}`).innerText)
        const liker_id = document.getElementById('current_user').innerText
        console.log(post_id)
        console.log(liker_id)
        fetch('/posting', {
            method: 'POST',
            body: JSON.stringify({post_id, liker_id})
        })
            .then(response => response.json())
            .then(result => {
                // Print result
                console.log(result);

        })
        //$( `#like-view${btn.dataset.postid}` ).load(` #like-view${btn.dataset.postid}` );
        document.querySelector(`#no-like-view${btn.dataset.postid}`).style.display = 'none';
        document.querySelector((`#like-view${btn.dataset.postid}`)).style.display = 'block';
        }
    })

  document.querySelectorAll('.remove_like').forEach(btn => {
    btn.onclick = function () {
        const post_id = parseInt(document.querySelector(`#current_post${btn.dataset.postid}`).innerText)
        const liker_id = document.getElementById('current_user').innerText
        console.log(post_id)
        console.log(liker_id)
        fetch('/posting', {
            method: 'DELETE',
            body: JSON.stringify({post_id, liker_id})
        })
            .then(response => response.json())
            .then(result => {
                // Print result
                console.log(result);

        })
        //$( `#no-like-view${btn.dataset.postid}` ).load(` #no-like-view${btn.dataset.postid} > *` );
        document.querySelector((`#like-view${btn.dataset.postid}`)).style.display = 'none';
        document.querySelector(`#no-like-view${btn.dataset.postid}`).style.display = 'block';
}

        }
        )



});



