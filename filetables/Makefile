glfiletable: glfiletable.c initparam
	gcc ${CFLAGS} -o glfiletable glfiletable.c ../common/init_params.c -lglusterfsclient

initparam: ../common/init_params.c
	gcc ${CFLAGS} -c ../common/init_params.c

clean:
	rm -f glfiletable *.o
