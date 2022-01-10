$BSSet = 4096, 8192, 16384, 32768, 65536, 131072, 1048576
$Rounds = 10

ForEach ($BS in $BSSet) {
		$DataFile = "test01_data_ss_detect_${BS}.csv"
		Add-Content $DataFile "Round, WriteIOPS"
		ForEach ($Pass in (1..$Rounds)) {
		$FioResults = (Get-Content "fio_pass=${Pass}_rw=0_bs=${BS}.json") -join "`n" | ConvertFrom-Json
		Add-Content $DataFile "$Pass, $($FioResults.jobs[0].write.iops)"
		}
}


