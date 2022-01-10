#!/usr/bin/gnuplot

set terminal svg size 800, 600 dynamic enhanced font "Liberation Sans, 12" rounded dashed background rgb 'white'
set output 'test03_ss_verify_cm6.svg'

set linetype 1 lw 1 lc rgb "#B20000" pointtype 7
set linetype 2 lw 1 lc rgb "#00B233"
set linetype 3 lw 1 lc rgb "#0000B2"
set linetype 4 lw 1 lc rgb "#B29200"
set linetype 5 lw 1 lc rgb "#000000"
set key box
set key below
set grid ytics
set xtics 1
set title "Steady State Verification"
set xlabel 'Round'
set ylabel 'Latency, ns'
set xrange [5:11]
#set yrange [40000:42000]

set style line 12 lc rgb '#808080' lt 0 lw 1
set grid back ls 12
set key bottom

set datafile separator ";"

f(x) = m*x + b
fit [6:10] f(x) 'test03_ss_bs=4096.csv' using 1:($2/1000000) every ::6::10 via m,b
stats 'test03_ss_bs=4096.csv' using ($2/1000000) every ::6::10 prefix "A"
plot 'test03_ss_bs=4096.csv' using 1:($2/1000000) every ::6::10 lt 1 notitle with points, \
'test03_ss_bs=4096.csv' using 1:($2/1000000) every ::6::10 lt 1 title 'IOPS' smooth csplines with lines, \
[6:10] m*x+b title 'Slope' dt (6,12,6,12), \
[6:10] A_mean title 'Average', \
[6:10]A_mean*1.1 title '110%*Average' lt 2, \
[6:10]A_mean*0.9 title '90%*Average' lt 2
set print "plot_ss_verify.log"
print A_mean, A_min, A_max, m, b
exit
