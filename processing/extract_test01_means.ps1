$RWMixSet = 100, 95, 65, 50, 35, 5, 0
$BSSet = 4096, 8192, 16384, 32768, 65536, 131072, 1048576

$Test_Data = @()

ForEach ($RWMix in $RWMixSet) {
	ForEach ($BS in $BSSet) {
		ForEach ($Pass in (6..10)) {
		$FioResults = (Get-Content "fio_pass=${Pass}_rw=${RWMix}_bs=${BS}.json") -join "`n" | ConvertFrom-Json
		$testRow = New-Object -TypeName PSObject
		$testRow | Add-Member -Type NoteProperty -Name Round -Value $Pass
		$testRow | Add-Member -Type NoteProperty -Name BS -Value $BS
		$testRow | Add-Member -Type NoteProperty -Name RWMix -Value $RWMix
		$testRow | Add-Member -Type NoteProperty -Name ReadIOPS -Value $($FioResults.jobs[0].read.iops)
		$testRow | Add-Member -Type NoteProperty -Name WriteIOPS -Value $($FioResults.jobs[0].write.iops)
		$testRow | Add-Member -Type NoteProperty -Name TotalIOPS -Value $($testRow.ReadIOPS + $testRow.WriteIOPS)
		$Test_Data += $testRow
		}
	}
}

$Test_Data_Averaged = @()

ForEach ($AvGroup in (0..48)) {
	$testRowAveraged = New-Object -TypeName PSObject
	$testRowAveraged | Add-Member -Type NoteProperty -Name BS -Value $Test_Data[$($AvGroup * 5)].BS
	$testRowAveraged | Add-Member -Type NoteProperty -Name RWMix -Value $Test_Data[$($AvGroup * 5)].RWMix
	$IOPS_Set = @()
	ForEach ($AvRow in (0..4)) {
		$IOPS_Set += $Test_Data[$($AvGroup * 5 + $AvRow)].TotalIOPS
	}
	$testRowAveraged | Add-Member -Type NoteProperty -Name AverageIOPS -Value $([math]::Round($($IOPS_Set | Measure-Object -Average | select -expand Average)))
	$Test_Data_Averaged += $testRowAveraged
}

$Test_Data_Averaged | Export-Csv test01_averaged.csv -Delimiter ";" -NoTypeInformation