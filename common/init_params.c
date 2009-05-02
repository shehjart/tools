

#include <stdio.h>
#include <libglusterfsclient.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

#define DEFAULT_LOOKUP_TIMEO    0
#define DEFAULT_STAT_TIMEO      0


void
gip_usage ()
{
        fprintf (stderr, "-l    <logfile-path>\n");
        fprintf (stderr, "-L    <LOGLEVEL>\n");
        fprintf (stderr, "-f    <volfile-path>\n");
        fprintf (stderr, "-v    <volume-name>\n");

}

glusterfs_init_params_t *
get_init_params (char * argv[], int argc)
{
        glusterfs_init_params_t *ipars = NULL;
        int                     i = 0;

        ipars = calloc (1, sizeof(glusterfs_init_params_t));
        assert (ipars);

        for (; i < argc; i++) {
                
                if (strcmp (argv[i], "-l") == 0) {
                        ipars->logfile = strdup (argv[++i]);
                        continue;
                }

                if (strcmp (argv[i], "-L") == 0) {
                        ipars->loglevel = strdup (argv[++i]);
                        continue;
                }

                if (strcmp (argv[i], "-f") == 0) {
                        ipars->specfile = strdup (argv[++i]);
                        continue;
                }

                if (strcmp (argv[i], "-v") == 0) {
                        ipars->volume_name = strdup (argv[++i]);
                        continue;
                }

        }

        if (!ipars->specfile) {
                fprintf (stderr, "Must specify vol file using -f\n");
                goto free_out;
        }

        if (!ipars->volume_name) {
                fprintf (stderr, "Must specify volume name using -v\n");
                goto free_out;
        }

        ipars->lookup_timeout = DEFAULT_LOOKUP_TIMEO;
        ipars->stat_timeout = DEFAULT_STAT_TIMEO;

        return ipars;

free_out:
        free (ipars);
        return NULL;
}


