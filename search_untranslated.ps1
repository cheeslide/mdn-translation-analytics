$en_folder = ".\content\files\en-us" # CHANGE IT
$zh_folder = ".\translated-content\files\zh-cn" # CHANGE IT
$output_file = ".\untranslated.txt"

Get-ChildItem -Path $en_folder -Recurse -File -Filter "*.md" | `
Select-Object -ExpandProperty FullName | `
ForEach-Object {
    $relative_path = $_ -replace [regex]::Escape($en_folder), ""
    $zh_file = Join-Path -Path $zh_folder -ChildPath $relative_path
    if (!(Test-Path -Path $zh_file)) {
        $relative_path
    }
} | Out-File -FilePath $output_file -Encoding UTF8