// Dylan Greene, 31 January 2017
// A custom shell similar everyday shells which is capable of executing,
// managing, and monitoring user level programs.

// Includes
#include <stdio.h> // printf, fgets, and fflush
#include <unistd.h> // fork and exec syscalls
#include <sys/types.h> // pid_t
#include <sys/wait.h> // wait syscall
#include <stdlib.h> // exit and atoi
#include <string.h> // strerror, strcmp, strsignal, and strtok
#include <errno.h> // errno
#include <signal.h> // kill and signals

// Constants
#define TRUE 1
#define FALSE 0
#define BUFFSIZE 4097
#define MAXWORDS 100

// Function Prototypes
void startfunc(char *args[]);
void waitfunc();
void runfunc(char *args[]);
void signalfunc(char *args[], int sig);

// Main Execution
int main(int argc, char * argv[]){
    // Ensure proper usage
    if(argc != 1){
        fprintf(stderr, "Usage: %s\n", argv[0]);
        exit(1);
    }

    // Keep running the shell until user quits
    int loop = TRUE;
    while(loop){
        // Print the prompt
        printf("myshell> ");
        fflush(stdout);

        // Gather input line
        char buff[BUFFSIZE];
        if(fgets(buff, BUFFSIZE, stdin) == NULL){
            printf("myshell: Reached EOF\n");
            exit(0);
        }

        // Check for just an enter
        if(strcmp(buff, "\n") == 0) continue;

        // Parse first word of input
        char *action = strtok(buff, " \t\n");

        // Check for a blank input (just whitespce)
        if(action == NULL) continue;

        // Check if it should exit
        if(strcmp(action, "quit") == 0) exit(0);
        if(strcmp(action, "exit") == 0) exit(0);

        // Parse remainder of input into args array
        char *arg = strtok(NULL, " \t\n");
        char *args[MAXWORDS + 1];
        int i = 0, nWords = 0;
        for(i = 0; arg != NULL; i++){
            if(i == MAXWORDS){
                fprintf(stderr, "myshell: Input line can be a maximum of %d args\n", MAXWORDS);
                break;
            }
            args[i] = arg;
            nWords++;
            arg = strtok(NULL, " \t\n");
        }
        if(i == MAXWORDS) continue;
        args[nWords] = NULL;

        // Check what the command is and act on it appropriately
        if(strcmp(action, "start") == 0) startfunc(args);
        else if(strcmp(action, "wait") == 0) waitfunc();
        else if(strcmp(action, "run") == 0) runfunc(args);
        else if(strcmp(action, "kill") == 0) signalfunc(args, SIGKILL);
        else if(strcmp(action, "stop") == 0) signalfunc(args, SIGSTOP);
        else if(strcmp(action, "continue") == 0) signalfunc(args, SIGCONT);
        else fprintf(stderr, "myshell: Invalid command: %s\n", action);
    }
    return 0;
}

// Function Implementations

void startfunc(char *args[]){
    if(args[0] == NULL){
        fprintf(stderr, "myshell: Not enough arguments passed\n");
        return;
    }
    // Fork to create child that execs
    pid_t pid = fork();

    if(pid < 0){ // Fork failed
        perror("myshell: Fork failed");
    }else if(pid == 0){ // Child
        if(execvp(args[0], args) < 0){
            perror("myshell: Unable to exec");
        }
    }else{ // Parent
        printf("myshell: Process %ld started\n", (long)pid);
        return;
    }
}

void waitfunc(){
    int status;
    pid_t tid = wait(&status);
    if(tid < 0){
        perror("myshell: Wait failed");
    }else{
        if(WIFEXITED(status)) printf("myshell: Process %ld exited normally with status %d\n", (long)tid, status);
        else if(WIFSIGNALED(status)) fprintf(stderr, "myshell: Process %ld exited abnormally with signal %d: %s\n", (long)tid, WTERMSIG(status), strsignal(WTERMSIG(status)));
        else fprintf(stderr, "myshell: Process %ld exited abnormally with status %d\n", (long)tid, status);
    }
}

// Combines the functionality of start and wait
void runfunc(char *args[]){
    if(args[0] == NULL){
        fprintf(stderr, "myshell: Not enough arguments passed\n");
        return;
    }
    // Fork to create child that execs
    pid_t pid = fork();

    if(pid < 0){ // Fork failed
        perror("myshell: Fork failed");
    }else if(pid == 0){ // Child
        if(execvp(args[0], args) < 0){
            perror("myshell: Unable to exec");
        }
    }else{ // Parent
        int status;
        pid_t tid = waitpid(pid, &status, 0);
        if(tid < 0) perror("myshell: Wait failed");
        if(WIFEXITED(status)) printf("myshell: Process %ld exited normally with status %d\n", (long)tid, status);
        else if(WIFSIGNALED(status)) fprintf(stderr, "myshell: Process %ld exited abnormally with signal %d: %s\n", (long)tid, WTERMSIG(status), strsignal(WTERMSIG(status)));
        else fprintf(stderr, "myshell: Process %ld exited abnormally with status %d\n", (long)tid, status);
    }
}

// Used for kill, stop and continue
void signalfunc(char *args[], int sig){
    if(args[0] == NULL){
        fprintf(stderr, "myshell: PID not passed\n");
        return;
    }
    pid_t pid = atoi(args[0]);
    if(pid == 0){
        fprintf(stderr, "myshell: Must pass a numeric PID\n");
        return;
    }
    if(kill(pid, sig) == 0) printf("myshell: Process %ld %s\n", (long)pid, strsignal(sig));
    else perror("myshell");
}
