$logFile = "md_logs.txt"
$outFile = "old_files.csv"
$targetFiles = "current_files.txt"
git log --format=%ad --date=short --name-only | Out-File -FilePath $logFile -Encoding ascii
git ls-files *.md | Out-File -FilePath $targetFiles -Encoding ascii
python old.py $logFile $outFile $targetFiles