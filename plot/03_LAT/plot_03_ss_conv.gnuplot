#!/usr/bin/gnuplot

set terminal svg size 800, 600 dynamic enhanced font "Liberation Sans, 12" rounded dashed background rgb 'white'
set output 'test03_ss_conv_cm6.svg'

set linetype 1 lw 1 lc rgb "#B20000" pointtype 9
set linetype 2 lw 1 lc rgb "#00B233" pointtype 9
set linetype 3 lw 1 lc rgb "#0000B2" pointtype 9
set linetype 4 lw 1 lc rgb "#B29200" pointtype 9
set linetype 5 lw 1 lc rgb "#8400B2" pointtype 9
set linetype 6 lw 1 lc rgb "#000000" pointtype 9
set linetype 7 lw 1 lc rgb "#00B2B2" pointtype 9

set style line 11 lc rgb '#808080' lt 1

set border 3 back ls 11
set tics nomirror

set style line 12 lc rgb '#808080' lt 0 lw 1
set grid back ls 12
set key ins vert
set key bottom

set datafile separator ";"

#set xtics 10
#set ytics (0.1, 0.2, 0.3, 0.4, 0.8, 1, 2, 3 , 10, 12, 50, 100, 200)
set yrange [0: ]
#set xrange [0:180]
#set logscale y
set title "CM6 SS Convergence"
set xlabel 'Round'
set ylabel 'Latency, ms'
plot "test03_ss_bs=512.csv" using 1:($2/1000000) every ::1 notitle with points linestyle 1, \
"" using 1:($2/1000000) every ::1 notitle smooth csplines with lines linestyle 1, \
1 / 0 title "BS=0.5k" with linespoints linestyle 1, \
"test03_ss_bs=4096.csv" using 1:($2/1000000) every ::1 notitle with points linestyle 2, \
"" using 1:($2/1000000) every ::1 notitle smooth csplines with lines linestyle 2, \
1 / 0 title "BS=4k" with linespoints linestyle 2, \
"test03_ss_bs=8192.csv" using 1:($2/1000000) every ::1 notitle with points linestyle 3, \
"" using 1:($2/1000000) every ::1 notitle smooth csplines with lines linestyle 3, \
1 / 0 title "BS=8k" with linespoints linestyle 3
exit