$RWMixSet = 100, 70, 0
$BSSet = 4096, 8192
$TCSet = 1, 2, 4
$QDSet = 1, 2, 4, 8, 16, 32

$Test_Data = @()

ForEach ($TC in $TCSet) {
	ForEach ($QD in $QDSet) {
		ForEach ($RWMix in $RWMixSet) {
			ForEach ($BS in $BSSet) {
				ForEach ($Pass in (1..5)) {
					$FioResults = (Get-Content "fio_pass=$($Pass)_QD=$($QD)_TC=$($TC)_rw=$($RWMix)_bs=$($BS).json") -join "`n" | ConvertFrom-Json
					$testRow = New-Object -TypeName PSObject
					$testRow | Add-Member -Type NoteProperty -Name Round -Value $Pass
					$testRow | Add-Member -Type NoteProperty -Name BS -Value $BS
					$testRow | Add-Member -Type NoteProperty -Name RWMix -Value $RWMix
					$testRow | Add-Member -Type NoteProperty -Name TC -Value $TC
					$testRow | Add-Member -Type NoteProperty -Name QD -Value $QD
					$testRow | Add-Member -Type NoteProperty -Name Read_IOPS -Value $($FioResults.jobs[0].read.iops)
					$testRow | Add-Member -Type NoteProperty -Name Read_AveLat -Value $($FioResults.jobs[0].read.clat_ns.mean)
					$testRow | Add-Member -Type NoteProperty -Name Read_LatP99 -Value $($FioResults.jobs[0].read.clat_ns.percentile."99.000000")
					$testRow | Add-Member -Type NoteProperty -Name Read_LatP99d9 -Value $($FioResults.jobs[0].read.clat_ns.percentile."99.900000")
					$testRow | Add-Member -Type NoteProperty -Name Read_LatP99d99 -Value $($FioResults.jobs[0].read.clat_ns.percentile."99.990000")
					$testRow | Add-Member -Type NoteProperty -Name Read_MaxLat -Value $($FioResults.jobs[0].read.clat_ns.max)
					$testRow | Add-Member -Type NoteProperty -Name Write_IOPS -Value $($FioResults.jobs[0].write.iops)
					$testRow | Add-Member -Type NoteProperty -Name Write_AveLat -Value $($FioResults.jobs[0].write.clat_ns.mean)
					$testRow | Add-Member -Type NoteProperty -Name Write_LatP99 -Value $($FioResults.jobs[0].write.clat_ns.percentile."99.000000")
					$testRow | Add-Member -Type NoteProperty -Name Write_LatP99d9 -Value $($FioResults.jobs[0].write.clat_ns.percentile."99.900000")
					$testRow | Add-Member -Type NoteProperty -Name Write_LatP99d99 -Value $($FioResults.jobs[0].write.clat_ns.percentile."99.990000")
					$testRow | Add-Member -Type NoteProperty -Name Write_MaxLat -Value $($FioResults.jobs[0].write.clat_ns.max)
					$testRow | Add-Member -Type NoteProperty -Name Total_IOPS -Value $($testRow.Read_IOPS + $testRow.Write_IOPS)
					$testRow | Add-Member -Type NoteProperty -Name Total_AveLat -Value $($testRow.Read_AveLat + $testRow.Write_AveLat)
					$testRow | Add-Member -Type NoteProperty -Name Total_LatP99 -Value $($testRow.Read_LatP99 + $testRow.Write_LatP99)
					$testRow | Add-Member -Type NoteProperty -Name Total_LatP99d9 -Value $($testRow.Read_LatP99d9 + $testRow.Write_LatP99d9)
					$testRow | Add-Member -Type NoteProperty -Name Total_LatP99d99 -Value $($testRow.Read_LatP99d99 + $testRow.Write_LatP99d99)
					$testRow | Add-Member -Type NoteProperty -Name Total_MaxLat -Value $($testRow.Read_MaxLat + $testRow.Write_MaxLat)
					$Test_Data += $testRow
				}
			}
		}
	}
}
$Test_Data | Export-Csv test03.csv -Delimiter ";" -NoTypeInformation

$Test_Data_Averaged = @()

ForEach ($AvGroup in (0..143)) {
	$testRowAveraged = New-Object -TypeName PSObject
	$testRowAveraged | Add-Member -Type NoteProperty -Name BS -Value $Test_Data[$($AvGroup * 5)].BS
	$testRowAveraged | Add-Member -Type NoteProperty -Name RWMix -Value $Test_Data[$($AvGroup * 5)].RWMix
	$testRowAveraged | Add-Member -Type NoteProperty -Name TC -Value $Test_Data[$($AvGroup * 5)].TC
	$testRowAveraged | Add-Member -Type NoteProperty -Name QD -Value $Test_Data[$($AvGroup * 5)].QD
	$IOPS_Set = @()
	$AveLat_Set = @()
	$LatP99_Set = @()
	$LatP99d9_Set = @()
	$LatP99d99_Set = @()
	$MaxLat_Set = @()
	ForEach ($AvRow in (0..4)) {
		$IOPS_Set += $Test_Data[$($AvGroup * 5 + $AvRow)].Total_IOPS
		$AveLat_Set += $Test_Data[$($AvGroup * 5 + $AvRow)].Total_AveLat
		$LatP99_Set += $Test_Data[$($AvGroup * 5 + $AvRow)].Total_LatP99
		$LatP99d9_Set += $Test_Data[$($AvGroup * 5 + $AvRow)].Total_LatP99d9
		$LatP99d99_Set += $Test_Data[$($AvGroup * 5 + $AvRow)].Total_LatP99d99
		$MaxLat_Set += $Test_Data[$($AvGroup * 5 + $AvRow)].Total_MaxLat
	}
	$testRowAveraged | Add-Member -Type NoteProperty -Name IOPS -Value $([math]::Round($($IOPS_Set | Measure-Object -Average | select -expand Average)))
	$testRowAveraged | Add-Member -Type NoteProperty -Name AveLat -Value $($AveLat_Set | Measure-Object -Average | select -expand Average)
	$testRowAveraged | Add-Member -Type NoteProperty -Name LatP99 -Value $($LatP99_Set | Measure-Object -Average | select -expand Average)
	$testRowAveraged | Add-Member -Type NoteProperty -Name LatP99d9 -Value $($LatP99d9_Set | Measure-Object -Average | select -expand Average)
	$testRowAveraged | Add-Member -Type NoteProperty -Name LatP99d99 -Value $($LatP99d99_Set | Measure-Object -Average | select -expand Average)
	$testRowAveraged | Add-Member -Type NoteProperty -Name MaxLat -Value $($MaxLat_Set | Measure-Object -Average | select -expand Average)
	$Test_Data_Averaged += $testRowAveraged
}

$Test_Data_Averaged | Export-Csv test03_averaged.csv -Delimiter ";" -NoTypeInformation