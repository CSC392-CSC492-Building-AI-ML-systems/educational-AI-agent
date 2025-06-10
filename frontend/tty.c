#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pty.h>
#include <utmp.h>
#include <fcntl.h>
#include <string.h>
#include <sys/select.h>
#include <sys/wait.h>


int main(){


	int master_fd;
	pid_t pid;

	// creates a "pseudoterminal" and forks a child process
	pid = forkpty(&master_fd, NULL, NULL, NULL);

	if (pid < 0) {
		perror("forkpty");
		exit(1);
	}
	else if (pid == 0){ // then child process (it is the slave end of the pty)

		// b/c we used forkpty, in child, shell gets stdin, stdout, and stderr connected to the slave end of the pty
		// so we can just execute a shell here, and it will be connected to the pty

		// execute a shell in the child process (connect it to a shell)
		execlp("bash", "bash", NULL);
		perror("execlp");
		exit(1);
	}
	else { // parent process (it is the master end of the pty)
		char buffer[256];
		fd_set read_fds;
		int nbytes;

		while (1) {
            FD_ZERO(&read_fds);
            FD_SET(master_fd, &read_fds);
            FD_SET(STDIN_FILENO, &read_fds);

            int maxfd = (master_fd > STDIN_FILENO ? master_fd : STDIN_FILENO) + 1;

            if (select(maxfd, &read_fds, NULL, NULL, NULL) < 0) {
                perror("select");
                exit(1);
            }


            // If shell has output
            if (FD_ISSET(master_fd, &read_fds)) {
                nbytes = read(master_fd, buffer, sizeof(buffer) - 1);
                if (nbytes < 0) {
                    perror("read");
                    exit(1);
                } else if (nbytes == 0) {
                    break; // EOF
                }
                buffer[nbytes] = '\0';
                printf("%s", buffer); // print output from the shell
                fflush(stdout);
            }

            // If user typed something
            if (FD_ISSET(STDIN_FILENO, &read_fds)) {
                nbytes = read(STDIN_FILENO, buffer, sizeof(buffer));
                if (nbytes < 0) {
                    perror("read stdin");
                    exit(1);
                } else if (nbytes == 0) {
                    break; // EOF
                }
                write(master_fd, buffer, nbytes); // send input to shell
            }
		}

		waitpid(pid, NULL, 0); // wait for child process to finish
		close(master_fd);
	}
	return 0;	


}