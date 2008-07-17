/*
 *    Test code for fallocation support. 
 *    Copyright (C) 2007 Shehjar Tikoo, <shehjart@gelato.unsw.edu.au>
 *    More info is available at:
 *    http://www.gelato.unsw.edu.au/IA64wiki/NFSBenchmarking
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


#include <stdio.h>
#include <errno.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>
#include <inttypes.h>
#include <sys/time.h>
#include <sys/vfs.h>

//fallocate requirements in case glibc is not up to date.
//For ia64.
#define __NR_fallocate                1303

#define FALLOC_FL_KEEP_SIZE	0x01
#define FALLOC_ALLOCATE		0x0
#define FALLOC_RESV_SPACE	FALLOC_FL_KEEP_SIZE


#define timeval_to_usecs(ts) (((u_int64_t)ts.tv_sec * 1000000) + ts.tv_usec)

#define FLAG_DONT_UNLINK	0x1
#define FLAG_VERBOSE		0x2



#define FL_DONTUNLINK(flags) ((flags) & FLAG_DONT_UNLINK)
#define FL_VERBOSE(flags) ((flags) & FLAG_VERBOSE)



struct run_params {
	u_int64_t startoff;
	u_int64_t wrblksize;
	u_int64_t filesize;
	u_int64_t falloc_blksize;
	int runcount;
	char * filename;
	char * runfile;
	int fd;
	char * data;
	u_int64_t flags;
};

void
write_file(struct run_params rp)
{
	u_int64_t written, offset, to_write;
	u_int64_t falloc_limit = 0;
	int ret;

	for(offset = rp.startoff; offset < rp.filesize; offset += written) {
		written = write(rp.fd, rp.data, rp.wrblksize);
		if(FL_VERBOSE(rp.flags))
			fprintf(stderr, "offset: %"PRIu64", written: %"PRIu64"\n",
					offset, written);
		if (written < 0) {
			fprintf(stderr, "Error writing to file: %s: %s\n",
					rp.runfile, strerror(errno));
			return;
		}

		if((offset + rp.wrblksize) > falloc_limit) {
			ret = syscall(__NR_fallocate, rp.fd, FALLOC_FL_KEEP_SIZE,
					offset, rp.falloc_blksize);
			if(FL_VERBOSE(rp.flags))
				fprintf(stderr, "fallocate offset: %"PRIu64"\n",
						offset);

			if(ret < 0) {
				fprintf(stderr, "Could not fallocate %"PRIu64
						" bytes at offset %"PRIu64" :%s\n",
						rp.falloc_blksize, offset, 
						strerror(errno));
				return;
			}
			
			falloc_limit = offset + rp.falloc_blksize;
		}
	}
}


int
write_fallocate_test(struct run_params rp)
{
	int i;
	char runstr[10], runfile[50];

	rp.data = (char *)malloc(sizeof(char) * rp.wrblksize);
	if (rp.data == NULL) {
		fprintf(stderr, "Could not allocate memory: %s\n", strerror(errno));
		return -1;
	}
	memset(rp.data, 5, rp.wrblksize); 

	for(i = 1; i <= rp.runcount; i++) {
		sprintf(runstr, "%d", i);
		strcpy(runfile, rp.filename);
		strcat(runfile, runstr);
		rp.runfile = runfile;

		fprintf(stderr, "RUN %d: writing to file %s\n", i, runfile);
		rp.fd = open(runfile, O_CREAT | O_WRONLY, S_IRUSR | S_IWUSR);
		if(rp.fd < 0) {
			fprintf(stderr, "Could not create file: %s: %s\n",
					runfile, strerror(errno));
			return -1;
		}

		write_file(rp);

		if(!FL_DONTUNLINK(rp.flags))
			unlink(runfile);
	}

	
	return 0;
}


void init_runparams(struct run_params *rp)
{
	
	//Default values.
	rp->startoff = 0;
	rp->wrblksize = 0;
	rp->falloc_blksize = 0;
	rp->filesize = 0;
	rp->runcount = 1;
	rp->filename = NULL;
	rp->runfile = NULL;
	rp->fd = 0;
	rp->flags = 0;
};


void
usage()
{
	fprintf(stdout, "USAGE: \n");
	fprintf(stdout, "\t\t--filesize <filesize>\n");
	fprintf(stdout, "\t\t--wrblksize <blksize>\n");
	fprintf(stdout, "\t\t--fallocate <blksize>\n");
	fprintf(stdout, "\t\t--startoff <offset>\n"
			"\t\t\tNOTE: Default starting offset is 0.\n");
	fprintf(stdout, "\t\t--filename <filename>\n");
	fprintf(stdout, "\t\t--runcount <count>\n"
			"\t\t\tNOTE: Default runcount is 1.\n");
	fprintf(stdout, "\t\t--nounlink\n"
			"\t\t\tNOTE: By default, all test files are removed.\n");
	fprintf(stdout, "\t\t--verbose\n");
	
}
	



int 
main(int argc, char *argv[])
{
	char *fname = NULL;
	int i;
	struct run_params rp;
	char *endptr = NULL;

	if(argc < 8) {
		fprintf(stderr, "Not enough arguments\n");
		usage();
		return -1;
	}

	init_runparams(&rp);
	for(i = 0; i < argc; i++) {
		if((strcmp(argv[i], "--runcount")) == 0) {
			rp.runcount = atoi(argv[++i]);
			continue;
		}

		if((strcmp(argv[i], "--filesize")) == 0) {
			rp.filesize = strtoll(argv[++i], &endptr, 10);
			continue;
		}
	
		if((strcmp(argv[i], "--wrblksize")) == 0) {
			rp.wrblksize = strtoll(argv[++i], &endptr, 10);
			continue;
		}

		if((strcmp(argv[i], "--filename")) == 0) {
			fname = argv[++i];
			continue;
		}

		if((strcmp(argv[i], "--startoff")) == 0) {
			rp.startoff = strtoll(argv[++i], &endptr, 10);
			continue;
		}
		
		if((strcmp(argv[i], "--fallocate")) == 0) {
			rp.falloc_blksize = strtoll(argv[++i], &endptr, 10);
			continue;
		}

		if((strcmp(argv[i], "--nounlink")) == 0) {
			rp.flags |= FLAG_DONT_UNLINK;
			continue;
		}

		if((strcmp(argv[i], "--verbose")) == 0) {
			rp.flags |= FLAG_VERBOSE;
			continue;
		}

	}

	if(fname == NULL) {
		fprintf(stderr, "No filename given\n");
		usage();
		return -1;
	}
	else
		rp.filename = fname;

	if(rp.wrblksize == 0) {
		fprintf(stderr, "No wrblksize given.\n");
		usage();
		return -1;
	}

	if(rp.filesize == 0) {
		fprintf(stderr, "No filesize given.\n");
		usage();
		return -1;
	}

	if(rp.falloc_blksize == 0) {
		fprintf(stderr, "No fallocate blksize given.\n");
		usage();
		return -1;
	}

	fprintf(stderr, "filename %s, filesize %"PRIu64", writeblksize %"PRIu64
			", fallocate blksize %"PRIu64", offset %"PRIu64
			", runs %d\n", rp.filename, rp.filesize, rp.wrblksize,
			rp.falloc_blksize, rp.startoff, rp.runcount);
	
	write_fallocate_test(rp);

	return 0;
}
