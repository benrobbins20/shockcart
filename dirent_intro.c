#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <dirent.h>
#include <string.h>
#include <time.h>


int listdir(const char *path){ // char path is a pointer
    struct dirent *entry; //structure of the dirent library (.h files are called header files??) again its a pointer
    DIR *dp; //i guess dir is a type DIR directory path is a pointer
    dp = opendir(path);
    if (dp == NULL){ // assuming this means if the directory doesn't exist error out
        perror("opendir");
        return -1; // this redirects to stderr in some manor??
    }
    while((entry = readdir(dp)))
        puts(entry->d_name);
    closedir(dp); // does exactly what it seems closes the directory dp (directory path)
    return 0; // pretty sure this is just quiet return 
}

//so int func is more or less just a helper function
// can now implement it into a main function



int main(int argc, char **argv){ //so argc is the number of args, argv is an array containing argument strings
    time_t t;
    time(&t);
    printf("Current time: %s\n",ctime(&t)); //ctime is similar to asctime i guess, couldn't care less
    // quick output test that a like a lot more than hello world 

    int counter = 1;
    if argc
}



