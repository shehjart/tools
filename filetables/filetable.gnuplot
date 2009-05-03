set terminal png enhanced font 22 size 480,320
set output "filetable.png"
set title "File Table Performance\n50000 File Creates, ext3, single test thread\ncreat Vs. glusterfs_creat" 
set xlabel "Number of Files" 
set ylabel "Creation Time (in usecs/file)" 
set xrange [0:50000]
set yrange [0:3000]
set ytics 500
set xtics 10000
set style data points
set pointsize .5
set key tmargin center horizontal
set border 4095 linetype -1 linewidth 1.000
plot "posix.dat" using 1:3 ti "Linux","gluster-old.dat" using 1:3 ti "glusterfs-O(n)", "gluster-new.dat" using 1:3 ti "glusterfs-O(1)";
