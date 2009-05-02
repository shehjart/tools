glfiletable: glfiletable.c initparam
	gcc -o glfiletable glfiletable.c ../common/init_params.c -lglusterfsclient

initparam: ../common/init_params.c
	gcc -c ../common/init_params.c

clean:
	rm -f glfiletable *.o
