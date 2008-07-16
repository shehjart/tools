#! /bin/sh
# Transpose a matrix: assumes all lines have same number
# of fields
# Modified from the original script here:
# http://eda.ee.nctu.edu.tw/~zephlin/O'Reilly/books/unix2/sedawk/ch13_09.htm


exec awk '
	NR == 1 {
		n = NF
		for (i = 1; i <= NF; i++)
			row[i] = $i
		next
	}
		
		
	{
		if (NF > n)
			n = NF
		for (i = 1; i <= NF; i++)
			row[i] = row[i] " " $i
	}

END {
	for (i = 1; i <= n; i++) {
		gsub("^ ", "", row[i])
		print row[i]
	}

	
}' ${1+"$@"}
