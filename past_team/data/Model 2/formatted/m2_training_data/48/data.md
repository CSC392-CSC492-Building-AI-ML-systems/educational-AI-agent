# Asciinema Recording Documentation: Cloning and Setting Up deerhacks-cms

## Overview
This recording demonstrates how to clone the `deerhacks-cms` repository into the `MCSS` directory and attempt to install the necessary packages using `yarn install`.

---

## Timeline Breakdown

### 1. **Cloning the Repository**
- **Command:** `git clone https://github.com/utmmcss/deerhacks-cms.git`
- **Output:**
    ```bash
    Cloning into 'deerhacks-cms'...
    remote: Enumerating objects: 230, done.
    remote: Counting objects: 0% (1/230)
    remote: Counting objects: 1% (3/230)
    remote: Counting objects: 2% (5/230)
    remote: Counting objects: 3% (7/230)
    remote: Counting objects: 4% (10/230)
    remote: Counting objects: 5% (12/230)
    remote: Counting objects: 6% (14/230)
    remote: Counting objects: 7% (17/230)
    remote: Counting objects: 8% (19/230)
    remote: Counting objects: 9% (21/230)
    remote: Counting objects: 10% (23/230)
    remote: Counting objects: 11%
    ```
- **Explanation:** The user successfully clones the `deerhacks-cms` repository into the `MCSS` directory using `git clone`.

### 2. **Attempting to Install Packages**
- **Command:** `yarn install`
- **Output:**
    ```bash
    The engine "node" is incompatible with this module. Expected version ">=16.0.0 <=20.x.x". Got "22.1.0"
    error Found incompatible module.
    info Visit https://yarnpkg.com/en/docs/cli/install for documentation about this command.
    ```
- **Explanation:** The user attempts to install the required packages for the `deerhacks-cms` project using `yarn install`. However, the installed Node.js version (`22.1.0`) is incompatible, and the project expects a version between `16.0.0` and `20.x.x`.

---

## Key Takeaways
- **Repository Cloning:** The user successfully clones the `deerhacks-cms` repository using `git clone`.
- **Node.js Version Incompatibility:** The attempt to install the necessary packages using `yarn install` fails due to an incompatible Node.js version (`22.1.0`). The project requires a Node.js version between `16.0.0` and `20.x.x`.
