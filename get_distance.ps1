$en_folder = ".\content\files\en-us" # CHANGE IT
$zh_folder = ".\translated-content\files\zh-cn" # CHANGE IT
$env:GIT_DIR = ".\content\.git"# CHANGE IT
$env:GIT_WORK_TREE = ".\content"# CHANGE IT

$commitDistances = [System.Collections.Generic.List[PSObject]]::new()
$badFrontMatter = [System.Collections.Generic.List[String]]::new()

Get-ChildItem -Path $zh_folder -Recurse -File -Filter "*.md" | `
Select-Object -ExpandProperty FullName | `
ForEach-Object {
    $file_start = -join (Get-Content -Path $_ -TotalCount 6)
	if($file_start -match "\s{1,}sourceCommit:\s?([0-9a-f]{40})"){
		$relative_path = $_ -replace [regex]::Escape($zh_folder), ""
		$en_file = Join-Path -Path $en_folder -ChildPath $relative_path
		$the_redundant_variable_to_remove_the_whitespace = $Matches[1]+"..HEAD"
		$commitDistances.add(
			[PSCustomObject]@{
				File = $_
				Distance = git rev-list --count $the_redundant_variable_to_remove_the_whitespace -- $en_file
				#FrontHash = $Matches[1]
				#CurrentHash = git log --format=%H -1 -- $en_file
			}
		)
		# Write-Host "$en_file"
		# Write-Host $the_redundant_variable_to_remove_the_whitespace
	} else {
		$badFrontMatter.add($_)
	}
}
$commitDistances.ToArray() | Export-Csv -Path "distances.csv" -NoTypeInformation
$badFrontMatter | Out-File -FilePath "bad.txt" -Encoding ascii