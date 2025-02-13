### 1. **Fetching Data from GitHub API**
- **Command:** `curl https://api.github.com/users/octocat`
- **Output:** `{"login": "octocat", "id": 1, "node_id": "MDQ6VXNlcjE=", "avatar_url": "https://avatars.githubusercontent.com/u/1?v=4"}`
- **Explanation:** The user fetches data from the GitHub API for the user `octocat`, including information like `login`, `id`, and `avatar_url`.

### 2. **Checking the Response Headers**
- **Command:** `curl -I https://api.github.com/users/octocat`
- **Output:** `HTTP/1.1 200 OK`
- **Explanation:** The user fetches the headers from the API to verify the response status is `200 OK`.

### 3. **Ending the Session**
- **Command:** `exit`
- **Output:** *(none)*
- **Explanation:** The user exits the session after testing the `curl` commands.