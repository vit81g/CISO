New-Item -Path "C:\Temp" -ItemType Directory -Force;
Get-ChildItem "C:\Program Files (x86)" -Filter "*.exe" -File -Recurse -Force -ErrorAction SilentlyContinue |
ForEach-Object {
    $sig = Get-AuthenticodeSignature -LiteralPath $_.FullName;
    [PSCustomObject]@{
        FileName = $_.Name;
        FullPath = $_.FullName;
        Status = $sig.Status;
        StatusMessage = $sig.StatusMessage;
        Signer = $sig.SignerCertificate.Subject;
        Issuer = $sig.SignerCertificate.Issuer;
        Thumbprint = $sig.SignerCertificate.Thumbprint;
        Company = $_.VersionInfo.CompanyName;
        Product = $_.VersionInfo.ProductName;
        FileVersion = $_.VersionInfo.FileVersion;
        Attributes = $_.Attributes;
        CreationTime = $_.CreationTime;
        LastWriteTime = $_.LastWriteTime;
    }
} | Export-Csv "C:\Temp\EXE_Signatures.csv" -NoTypeInformation -Encoding UTF8 -Delimiter ";"