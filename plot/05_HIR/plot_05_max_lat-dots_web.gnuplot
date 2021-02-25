#!/usr/bin/gnuplot

set terminal svg size 800, 600 dynamic enhanced fname 'Liberation Sans, Sans' fsize '12' rounded dashed background rgb 'white'
set output 'HIR_max_lat.svg'

set linetype 1 lw 1 lc rgb "#B20000"
set linetype 2 lw 1 lc rgb "#00B233"
set linetype 3 lw 1 lc rgb "#0000B2"
set linetype 4 lw 1 lc rgb "#B29200"
set linetype 5 lw 1 lc rgb "#8400B2"
set linetype 6 lw 1 lc rgb "#79B200"
set linetype 7 lw 1 lc rgb "#00B2B2"
set linetype 8 lw 1 lc rgb "#000000"
set linetype 9 lw 1 lc rgb "#b2b200"

set style line 11 lc rgb '#808080' lt 1

set border 3 back ls 11
set tics nomirror

set style line 12 lc rgb '#808080' lt 0 lw 1
set grid back ls 12

unset key
#set key box
#set key below

set xtics 60
#set ytics 2000
set xrange [0:930]
set yrange [4:300]
#set ytics (9, 10, 12, 15, 17, 20, 25)
set logscale y
set title "HIR maximum latency vs time"
set xlabel 'Time (minutes)'
set ylabel 'Latency, ms'
plot 'test05_data.csv' using ($1*10/60):($7/1000) every ::1::360 title 'State 1 AB' with points pointtype 7 pointsize 0.3, \
'test05_data.csv' using ($1*5/60+60):($7/1000) every ::361::720 title 'State 1 C' with points pointtype 7 pointsize 0.3 lt 8, \
'test05_data.csv' using ($1*15/60+60+30):($7/1000) every ::721::1080 title 'State 2 AB' with points pointtype 7 pointsize 0.3, \
'test05_data.csv' using ($1*5/60+60+30+90):($7/1000) every ::1081::1440 title 'State 2 C' with points pointtype 7 pointsize 0.3 lt 8, \
'test05_data.csv' using ($1*20/60+60+30+90+30):($7/1000) every ::1441::1800 title 'State 3 AB' with points pointtype 7 pointsize 0.3, \
'test05_data.csv' using ($1*5/60+60+30+90+30+120):($7/1000) every ::1801::2160 title 'State 3 C' with points pointtype 7 pointsize 0.3 lt 8, \
'test05_data.csv' using ($1*30/60+60+30+90+30+120+30):($7/1000) every ::2161::2520 title 'State 5 AB' with points pointtype 7 pointsize 0.3, \
'test05_data.csv' using ($1*5/60+60+30+90+30+120+30+180):($7/1000) every ::2521::2880 title 'State 5 C' with points pointtype 7 pointsize 0.3 lt 8, \
'test05_data.csv' using ($1*55/60+60+30+90+30+120+30+180+30):($7/1000) every ::2881::3240 title 'State 10 AB' with points pointtype 7 pointsize 0.3 lt 9, \
'test05_data.csv' using ($1*5/60+60+30+90+30+120+30+180+30+330):($7/1000) every ::3241::3600 title 'State 10 C' with points pointtype 7 pointsize 0.3 lt 8
exit
