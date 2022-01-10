p = subprocess.Popen(['fio', '--filename=' + str(args.Device),
                           '--iodepth=' + str(OIO), '--numjobs=' + str(TC),
                           '--bs=' + str(BS), '--ioengine=' + str(args.IOEngine),
                           '--rwmixread=' + str(RWMix),
                           '--output=' + TestName + '/results/' + JSONFileName] + FioArgs,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           universal_newlines=True)