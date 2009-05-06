#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Returns a pointer to the @n'th char matching
 * @c in string @str, starting the search from right or
 * end-of-string, rather than starting from left, as rindex
 * function does.
 */
char *
libgf_rrindex (char *str, int c, int n)
{
        int     len = 0;
        int     occurrence = 0;

        if (str == NULL)
                return NULL;

        len = strlen (str);
        /* Point to last character of string. */
        str += (len - 1);
        while (len > 0) {
                if ((int)*str == c) {
                        ++occurrence;
                        if (occurrence == n)
                                break;
                }
                --len;
                --str;
        }

        return str;
}

char *
libgf_trim_to_prev_dir (char * path)
{
        char    *idx = NULL;

        if (!path)
                return NULL;

        /* Check if we're already at root, if yes
         * then there is no prev dir.
         */
        if (strlen (path) == 1)
                return path;

        idx = libgf_rrindex (path, '/', 1);
        /* Move to the char after the / */
        ++idx;
        *idx = '\0';

        return path;
}

/* Performs a lightweight path resolution that only
 * looks for . and  .. and replaces those with the
 * proper names.
 *
 * FIXME: This is a stop-gap measure till we have full
 * fledge path resolution going in here.
 * Function returns path strdup'ed so remember to FREE the
 * string as required.
 */
char *
libgf_resolve_path_light (char *path)
{
        char            *respath = NULL;
        char            *saveptr = NULL;
        char            *tok = NULL;
        char            *mypath = NULL;
        int             len = 0;
        int             addslash = 0;

        if (!path)
                goto out;

        /* We dont as yet support relative paths anywhere in
         * the lib.
         */
        if (path[0] != '/')
                goto out;

        mypath = strdup (path);
        len = strlen (mypath);
        respath = calloc (strlen(mypath) + 1, sizeof (char));
        if (respath == NULL)
                goto out;

        /* The path only contains a / or a //, so simply add a /
         * and return.
         * This needs special handling because the loop below does
         * not allow us to do so through strtok.
         */
        if (((mypath[0] == '/') && (len == 1))
                        || (strcmp (mypath, "//") == 0)) {
                strcat (respath, "/");
                goto out;
        }

        tok = strtok_r (mypath, "/", &saveptr);
        addslash = 0;
        strcat (respath, "/");
        while (tok) {
                if (addslash) {
                        if ((strcmp (tok, ".") != 0)
                                        && (strcmp (tok, "..") != 0)) {
                                strcat (respath, "/");
                        }
                }

                if ((strcmp (tok, ".") != 0) && (strcmp (tok, "..") != 0)) {
                        strcat (respath, tok);
                        addslash = 1;
                } else if ((strcmp (tok, "..") == 0)) {
                        libgf_trim_to_prev_dir (respath);
                        addslash = 0;
                }

                tok = strtok_r (NULL, "/", &saveptr);
        }

out:
        if (mypath)
                free (mypath);
        return respath;
}


int
main (int argc, char *argv[])
{

        fprintf (stdout, "%s\n", libgf_resolve_path_light (argv [1]));
        return 0;
}

