/*
 *    Copyright (C) 2009 Shehjar Tikoo, <shehjartikoo@gmail.com>
 *
 *    This program is free software; you can redistribute it and/or modify
 *    it under the terms of the GNU General Public License as published by
 *    the Free Software Foundation; either version 2 of the License, or
 *    (at your option) any later version.
 *
 *    This program is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU General Public License for more details.
 *
 *    You should have received a copy of the GNU General Public License along
 *    with this program; if not, write to the Free Software Foundation, Inc.,
 *    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 */



#include <sys/stat.h>
#include <stdio.h>
#include <sys/types.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>
#include <unistd.h>

static void
usage ()
{
        fprintf (stderr,  "Not enough arguments\n");
        fprintf (stderr, "USAGE: fchown <filename|filepath>\n");
        return;
}


static int
file_fchown (char * fname, uid_t uid, gid_t gid)
{
        int     fd = 0;

        fd = open (fname, O_RDWR);
        if (fd < 0) {
                fprintf (stderr, "Error opening file: %s: %s\n",
                                fname, strerror (errno));
                return -1;
        }

        fprintf (stdout, "Changing ownner: %s\n", fname);
        if (fchown (fd, uid, gid) < 0) {
                fprintf(stderr, "Error changing owners: %s\n",
                                strerror(errno));
                close (fd);
                return -1;
        }

        close (fd);
        return 0;
}

int
main (int argc, char *argv[])
{
        int             fd;
        char            *path = NULL;
        struct stat     sbuf;
        uid_t           uid = 0;
        gid_t           gid = 0;

        if (argc < 2) {
                usage();
                return -1;
        }
        path = argv[1];

        if (stat (path, &sbuf) < 0) {
                fprintf (stderr, "Error stat'ing path: %s: %s\n", path,
                                strerror(errno));
                return -1;
        }

        if (S_ISREG (sbuf.st_mode))
                file_fchown (path, uid, gid);
        else {
                fprintf (stderr, "Not a regular file: %s\n", path);
                return 0;
        }

        return 0;
}
