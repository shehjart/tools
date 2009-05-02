#include <libglusterfsclient.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <errno.h>
#include <sys/time.h>
#include <inttypes.h>

#define timeval_to_usecs(ts)    (((u_int64_t)ts.tv_sec * 1000000) + ts.tv_usec)

extern glusterfs_init_params_t *
get_init_params (char * argv[], int argc);

extern void
gip_usage ();

void
usage ()
{
        fprintf (stderr, "--fd-count <openfile-count>\n");
        fprintf (stderr, "--silent\n");
        fprintf (stderr, "--dry-run\n");
        fprintf (stderr, "--posixtest\n");
        fprintf (stderr, "--glustertest\n");
        fprintf (stderr, "\t--posixtest and --glustertest are mutually \n");
        fprintf (stderr, "\texclusive. The last one specified on the command");
        fprintf (stderr, "\n\t line applies.\n");
        fprintf (stderr, "--test-path <path>\n");
        fprintf (stderr, "\tIn case of --glusterfstest, this is used as the");
        fprintf (stderr, "\t VMP.\n");

        gip_usage ();


        fprintf (stderr, "OUTPUT: Output is a three tuple"
                         " : <FD-COUNT> <TOTAL-TIME-IN-USECS> <USECS-PER-FD>"
                         "\n");

}

#define CREAT_POSIX     1
#define CREAT_GLUSTERFS 2

struct runcontrol {
        int     silent;
        int     dryrun;
        int     whichcreat;
        char    *testpath;
};


int
glusterfs_creat_test (char *fname)
{
        glusterfs_file_t        fh = NULL;
                
        fh = glusterfs_creat (fname, S_IRWXU);
        if (fh == NULL)
                return -1;

        return 0;
}

int
posix_creat_test (char *fname)
{
        int fd = 0;

        fd = creat (fname, S_IRWXU);
        if (fd == -1)
                return -1;

        return 0;
}

int
create_files (int fdcount, struct runcontrol *rc)
{
        int                     i = 0;
        char                    fname[1024];
        int                     err = 0;
        int                     ret = 0;

        for (; i < fdcount; i++) {
                sprintf(fname, "%s/%d.test", rc->testpath, i);
                if (!rc->silent)
                        fprintf (stdout, "Creating file %s\n", fname);

                err = 0;
                ret = 0;
                if (rc->dryrun)
                        continue;

                if (rc->whichcreat == CREAT_GLUSTERFS)
                        ret = glusterfs_creat_test (fname);
                else
                        ret = posix_creat_test (fname);

                err = errno;
                if (ret == -1) {
                        fprintf (stderr, "Error creating file: %s: %s\n",
                                 fname, strerror (err));
                        return -1;
                }
        }

        return 0;
}

int
run_glfiletable_test (int fdcount, struct runcontrol *rc)
{
        struct timeval  starttime, endtime;
        u_int64_t       startusecs, endusecs, duration;
        
        
        gettimeofday (&starttime, NULL);
        if (create_files (fdcount, rc) == -1)
                return -1;
        gettimeofday (&endtime, NULL);

        startusecs = timeval_to_usecs (starttime);
        endusecs = timeval_to_usecs (endtime);
        duration = endusecs - startusecs;

        fprintf (stdout, "%d %"PRIu64" %"PRIu64"\n", fdcount, duration,
                 (duration / fdcount));

        return 0;
}

int
main (int argc, char *argv[])
{
        glusterfs_init_params_t         *ipars = NULL;
        int                             fdcount = 0;
        int                             i = 0;
        char                            *fdptr = NULL;
        struct runcontrol               rc;

        memset (&rc, 0, sizeof (struct runcontrol));
        for (;i < argc; ++i) {
                if (strcmp (argv[i], "--fd-count") == 0) {
                        fdptr = argv[i+1];
                        continue;
                }

                if (strcmp (argv[i], "--silent") == 0) {
                        rc.silent = 1;
                        continue;
                }

                if (strcmp (argv[i], "--dry-run") == 0) {
                        rc.dryrun = 1;
                        continue;
                }

                if (strcmp (argv[i], "--posixtest") == 0) {
                        rc.whichcreat = CREAT_POSIX;
                        continue;
                }

                if (strcmp (argv[i], "--glusterfstest") == 0) {
                        rc.whichcreat = CREAT_GLUSTERFS;
                        continue;
                }

                if (strcmp (argv[i], "--test-path") == 0) {
                        rc.testpath = strdup (argv[i+1]);
                        continue;
                }

                if (strcmp (argv[i], "--help") == 0) {
                        usage ();
                        return 0;
                }

        }

        if (fdptr == NULL) {
                fprintf (stderr, "fd count not specified\n");
                usage ();
                return -1;
        }

        sscanf (fdptr, "%d", &fdcount);
        if (fdcount == 0) {
                fprintf (stderr, "Invalid value for fd count\n");
                usage ();
                return -1;
        }

        if (rc.whichcreat == 0) {
                fprintf (stderr, "Test type not specified\n");
                usage ();
                return -1;
        }

        if (rc.testpath == NULL) {
                fprintf (stderr, "Test path not specified\n");
                usage ();
                return -1;
        }

        if (rc.whichcreat == CREAT_GLUSTERFS) {
                ipars = get_init_params (argv, argc);
                if (ipars == NULL) {
                        usage ();
                        return -1;
                }

                if ((glusterfs_mount (rc.testpath, ipars)) < 0) {
                        fprintf (stderr, "Error mounting glusterfs\n");
                        return -1;
                }
        }

        run_glfiletable_test (fdcount, &rc);
        return 0;
}
