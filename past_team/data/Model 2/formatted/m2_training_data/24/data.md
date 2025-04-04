# Asciinema Recording Documentation: Setting Up MySQL Server

## Overview
This recording demonstrates the process of installing, configuring, and verifying a MySQL database server.

---

## Timeline Breakdown

### 1. **Installing MySQL Server**
- **Command:** `sudo apt install mysql-server`
- **Output:** `Setting up mysql-server (8.0)...`
- **Explanation:** The user installs the MySQL database server package, enabling database management on the system.

### 2. **Starting the MySQL Service**
- **Command:** `sudo systemctl start mysql`
- **Output:** `[ OK ] Starting MySQL Server`
- **Explanation:** The MySQL service is started to allow database interactions.

### 3. **Logging into MySQL**
- **Command:** `mysql -u root -p`
- **Output:** `Enter password:`
- **Explanation:** The user logs into MySQL as the root user to perform administrative tasks.

### 4. **Creating a New Database**
- **Command:** `CREATE DATABASE test_db;`
- **Output:** `Query OK, 1 row affected`
- **Explanation:** A new database named `test_db` is created for testing purposes.

### 5. **Ending the Session**
- **Command:** `exit`
- **Output:** *(none)*
- **Explanation:** The user exits the SSH session after completing the database setup process.

---

## Key Takeaways
- **Installation and Configuration:** Demonstrated setting up MySQL and starting its service.
- **Database Management:** Showcased creating a database using MySQL commands.