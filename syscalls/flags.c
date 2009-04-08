#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <stdio.h>


int
main ()
{

        fprintf (stdout, "O_RDONLY: %d\n",O_RDONLY);
        fprintf (stdout, "O_WRONLY: %d\n",O_WRONLY);
        fprintf (stdout, "O_RDWR: %d\n",O_RDWR);


        return 0;
}

