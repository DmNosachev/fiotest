#!/usr/bin/gnuplot

set terminal svg size 800, 600 dynamic enhanced font "Liberation Sans, 12" rounded dashed background rgb 'white'
set output 'iops-wsat.svg'

#set obj 1 rectangle behind from screen 0,0 to screen 1,1
#set obj 1 fillstyle solid 1.0 fillcolor rgbcolor "#F0F0F0"

set linetype 1 lw 1 lc rgb "#B20000"
set linetype 2 lw 1 lc rgb "#00B233"
set linetype 3 lw 1 lc rgb "#0000B2"
set style line 11 lc rgb '#808080' lt 1

set border 3 back ls 11
set tics nomirror

set style line 12 lc rgb '#808080' lt 0 lw 1
set grid back ls 12
set key box
set key below

set xtics 60
set ytics 20000
#set yrange [50000:]
set xrange [0:600]
set title "Write saturation test (random write 4K): IOPS"
set xlabel 'Time (minutes)'
set ylabel 'IOPS'
plot 'PTS_04 data.dat' using 1:2 every ::1 title 'Kingston KC2000 500GB' with lines
#'px02sm.dat' using 1:2 every ::1 title 'Toshiba PX02SM 200GB (PX02SMF020)' with lines
exit
