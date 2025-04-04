# Asciinema Recording Documentation: Backup and Restore with `rsync`

## Overview
This recording demonstrates using `rsync` to backup and restore data between directories.

---

## Timeline Breakdown

### 1. **Backing Up Data**
- **Command:** `rsync -av /source/ /backup/`
- **Output:** `sent 1000 bytes received 1000 bytes 2000.00 bytes/sec`
- **Explanation:** The user performs a backup from `/source/` to `/backup/` using `rsync`.

### 2. **Restoring Data**
- **Command:** `rsync -av /backup/ /restore/`
- **Output:** `sent 1000 bytes received 1000 bytes 2000.00 bytes/sec`
- **Explanation:** The user restores data from the `/backup/` directory to `/restore/`.

### 3. **Ending the Session**
- **Command:** `exit`
- **Output:** *(none)*
- **Explanation:** The user exits the session after completing the backup and restore tasks.

---

## Key Takeaways
- **Data Backup:** Demonstrated using `rsync` to create backups of files and directories.
- **Data Restoration:** Showed how to restore backed-up files using `rsync`.
