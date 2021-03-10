$TestName = 'PTS_05'

$DataFile = "$TestName data.dat"
Add-Content $DataFile "Round, IOPS, AveLat, LatP99, LatP99.9, LatP99.99, MaxLat"

ForEach ($StateName in ('State_1_AB', 'State_2_AB', 'State_3_AB', 'State_5_AB', 'State_10_AB')) {
	ForEach ($AccessName in ('AB', 'C')) {
		ForEach ($Pass in (1..360)) {
			$FioOutputJSONFile = "fio_$($StateName)_access-$($AccessName)_pass=$($Pass).json"
			$FioResults = (Get-Content $FioOutputJSONFile) -join "`n" | ConvertFrom-Json
			Add-Content $DataFile "$Pass, $($FioResults.jobs[0].write.iops), $($FioResults.jobs[0].write.clat_ns.mean), $($FioResults.jobs[0].write.clat_ns.percentile."99.000000"), $($FioResults.jobs[0].write.clat_ns.percentile."99.900000"), $($FioResults.jobs[0].write.clat_ns.percentile."99.990000"), $($FioResults.jobs[0].write.clat_ns.max)"
		}
	}
}
