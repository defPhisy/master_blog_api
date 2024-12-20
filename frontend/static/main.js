// Function that runs once the window is fully loaded
window.onload = function () {
  // Attempt to retrieve the API base URL from the local storage
  var savedBaseUrl = localStorage.getItem("apiBaseUrl");
  // If a base URL is found in local storage, load the posts
  if (savedBaseUrl) {
    document.getElementById("api-base-url").value = savedBaseUrl;
    loadPosts();
  }
};

// Function to fetch all the posts from the API and display them on the page
function loadPosts() {
  // Retrieve the base URL from the input field and save it to local storage
  var baseUrl = document.getElementById("api-base-url").value;
  localStorage.setItem("apiBaseUrl", baseUrl);

  // Use the Fetch API to send a GET request to the /posts endpoint
  fetch(baseUrl + "/posts")
    .then((response) => response.json()) // Parse the JSON data from the response
    .then((data) => {
      // Once the data is ready, we can use it
      // Clear out the post container first
      const postContainer = document.getElementById("post-container");
      postContainer.innerHTML = "";

      // For each post in the response, create a new post element and add it to the page
      data.forEach((post) => {
        const postDiv = document.createElement("div");
        postDiv.className = "post";
        postDiv.innerHTML = `<h2 class="title">${post.title}</h2>
                            <span class="author">${post.author}</span>
                            <span class="date">${post.date_created}</span>
                            <p class="content">${post.content}</p>
                            <button onclick="deletePost(${post.id})">Delete</button>`;
        postContainer.appendChild(postDiv);
      });
    })
    .catch((error) => console.error("Error:", error)); // If an error occurs, log it to the console
}

function addPost() {
  // Retrieve the input elements
  var baseUrl = document.getElementById("api-base-url").value;
  var postTitleInput = document.getElementById("post-title");
  var postAuthorInput = document.getElementById("post-author");
  var postContentInput = document.getElementById("post-content");

  // Retrieve the values from the input elements
  var postTitle = postTitleInput.value;
  var postAuthor = postAuthorInput.value;
  var postContent = postContentInput.value;

  // Use the Fetch API to send a POST request to the /posts endpoint
  fetch(baseUrl + "/posts", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      title: postTitle,
      content: postContent,
      author: postAuthor,
    }),
  })
    .then((response) => response.json()) // Parse the JSON data from the response
    .then((post) => {
      console.log("Post added:", post);
      loadPosts(); // Reload the posts after adding a new one

      // Reset the input fields
      postTitleInput.value = "";
      postAuthorInput.value = "";
      postContentInput.value = "";
    })
    .catch((error) => console.error("Error:", error)); // Log any errors
}

// Function to send a DELETE request to the API to delete a post
function deletePost(postId) {
  var baseUrl = document.getElementById("api-base-url").value;

  // Use the Fetch API to send a DELETE request to the specific post's endpoint
  fetch(baseUrl + "/posts/" + postId, {
    method: "DELETE",
  })
    .then((response) => {
      console.log("Post deleted:", postId);
      loadPosts(); // Reload the posts after deleting one
    })
    .catch((error) => console.error("Error:", error)); // If an error occurs, log it to the console
}

function sortPosts() {
  const sortField = document.getElementById("sorting-key").value;

  // Retrieve the base URL from the input field and save it to local storage
  var baseUrl = document.getElementById("api-base-url").value;
  localStorage.setItem("apiBaseUrl", baseUrl);

  // Use the Fetch API to send a GET request to the /posts endpoint
  fetch(baseUrl + `/posts?sort=${sortField}`)
    .then((response) => response.json()) // Parse the JSON data from the response
    .then((data) => {
      // Once the data is ready, we can use it
      // Clear out the post container first
      const postContainer = document.getElementById("post-container");
      postContainer.innerHTML = "";

      // For each post in the response, create a new post element and add it to the page
      data.forEach((post) => {
        const postDiv = document.createElement("div");
        postDiv.className = "post";
        postDiv.innerHTML = `<h2 class="title">${post.title}</h2>
                            <span class="author">${post.author}</span>
                            <span class="date">${post.date_created}</span>
                            <p class="content">${post.content}</p>
                            <button onclick="deletePost(${post.id})">Delete</button>`;
        postContainer.appendChild(postDiv);
      });
    })
    .catch((error) => console.error("Error:", error)); // If an error occurs, log it to the console
}
