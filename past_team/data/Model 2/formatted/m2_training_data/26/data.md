# Asciinema Recording Documentation: Deploying a Simple HTML Website with Nginx

## Overview
This recording demonstrates the installation, configuration, and deployment of a basic HTML website using the Nginx web server.

---

## Timeline Breakdown

### 1. **Installing Nginx**
- **Command:** `sudo apt install nginx`
- **Output:** `Setting up nginx...`
- **Explanation:** Installs the Nginx web server, which is widely used for serving web content.

### 2. **Starting the Nginx Service**
- **Command:** `sudo systemctl start nginx`
- **Output:** `[ OK ] Starting Nginx Web Server`
- **Explanation:** Starts the Nginx service to enable serving web content.

### 3. **Deploying the HTML File**
- **Command:** `echo '<h1>Welcome to My Website</h1>' | sudo tee /var/www/html/index.html`
- **Output:** `<h1>Welcome to My Website</h1>`
- **Explanation:** Creates a simple HTML homepage and deploys it to the default Nginx web root directory.

### 4. **Verifying the Deployment**
- **Command:** `curl http://localhost`
- **Output:** `<h1>Welcome to My Website</h1> `
- **Explanation:** Confirms that the Nginx server is correctly serving the deployed HTML content.

 ### 5. **Ending the Session**
- **Command:** `exit`
- **Output:** *(none)*
- **Explanation:** The user exits the session after successfully deploying and verifying the website.

---

## Key Takeaways
- **Web Server Setup:** Demonstrated installing and starting the Nginx web server.
- **Website Deployment:** Showcased deploying a simple HTML homepage using a one-liner command.
- **Verification:** Verified that the website was successfully served by Nginx.
- **Session Closure:** Documented the closure of the session with the `exit` command.