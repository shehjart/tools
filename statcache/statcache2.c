#include <stdio.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <string.h>
#include <dirent.h>
#include <errno.h>
#include <inttypes.h>
#include <dirent.h>
#include <sys/time.h>
#include <stdlib.h>

#define timeval_to_usecs(ts)    (((u_int64_t)ts.tv_sec * 1000000) + ts.tv_usec)


int
traverse_dir (char *path, int filecount)
{
        char                    statpath[1024];
        struct stat             sbuf;
        int                     i;
        
        for (i =0;i < filecount; i++) {
                sprintf (statpath, "%s/%d.test",path, i);
                if ((stat (statpath, &sbuf)) < 0) {
                        fprintf (stderr, "Error stat'ing file: %s\n",
                                 strerror (errno));
                        return -1;
                }
        }
 
        return 0;
}


void
stat_cache_test (char *path, int filecount)
{
        struct timeval          starttime, endtime;
        u_int64_t               startusecs, endusecs;
        
        gettimeofday (&starttime, NULL);
        if (traverse_dir (path, filecount) < 0)
                return;
        gettimeofday (&endtime, NULL);

        startusecs = timeval_to_usecs (starttime);
        endusecs = timeval_to_usecs (endtime);
        fprintf (stdout, "Run: %"PRIu64" usecs ", (endusecs-startusecs));
        fflush (stdout);

}


int
main (int argc, char *argv[])
{
        char    *path = NULL;
        int     i;
        int     sleepsec = 0;
        int     filecount = 0;

        for (i = 0; i < argc; i++) {
                if ((strcmp (argv[i], "--path")) == 0) {
                        path = argv[i+1];
                        continue;
                }

                if ((strcmp (argv[i], "--delay")) == 0) {
                        sleepsec = atoi (argv[i+1]);
                        continue;
                }

                if ((strcmp (argv[i], "--count")) == 0) {
                        filecount = atoi (argv[i+1]);
                        continue;
                }
        }

        if (path == NULL) {
                fprintf (stderr, "File name not given.\n");
                return -1;
        }

        fprintf (stdout, "Test: path %s, delay %d: ", path, sleepsec);
        fflush (stdout);
        stat_cache_test (path, filecount);
        sleep (sleepsec);
        stat_cache_test (path, filecount);
        fprintf (stdout, "\n");
        return 0;
}



