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
        fprintf (stderr, "USAGE: access <filename|filepath>\n");
        return;
}


static int
path_access (char * fname, int mode)
{
        fprintf (stdout, "Accessing file: %s\n", fname);
        if (access (fname, mode) < 0) {
                fprintf(stderr, "Error access()'ing: %s\n", strerror(errno));
                return -1;
        }

        return 0;
}

int
main (int argc, char *argv[])
{
        char    *path = NULL;
        int     mode = R_OK | W_OK | X_OK;

        if (argc < 2) {
                usage();
                return -1;
        }
        path = argv[1];

        path_access (path, mode);
        return 0;
}
