$locales = @("de", "en", "es", "fr", "it", "ja", "pt", "zh_Hans")
foreach ($lang in $locales) {
    $poPath = "locale\$lang\LC_MESSAGES\django.po"
    if (Test-Path $poPath) {
        Write-Host "Cleaning duplicates in $lang..."
        msguniq $poPath -o $poPath
    } else {
        Write-Host "Skipping $lang — file not found."
    }
}