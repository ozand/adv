[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^COM[1-9][0-9]*$')]
    [string]$Port,
    [ValidateRange(300, 2000000)]
    [int]$Baud = 115200,
    [ValidateRange(1, 20)]
    [int]$Seconds = 8
)

$ErrorActionPreference = 'Stop'
$serial = [System.IO.Ports.SerialPort]::new($Port, $Baud, 'None', 8, 'One')
$serial.ReadTimeout = 200
$serial.WriteTimeout = 200
$serial.DtrEnable = $false
$serial.RtsEnable = $false
$serial.Handshake = 'None'

try {
    $serial.Open()
    Write-Host "Passive RX only on $Port at $Baud baud for $Seconds seconds. No TX; DTR/RTS disabled."
    $deadline = [DateTime]::UtcNow.AddSeconds($Seconds)
    $buffer = New-Object byte[] 512
    $total = 0
    while ([DateTime]::UtcNow -lt $deadline -and $total -lt 8192) {
        try {
            $read = $serial.Read($buffer, 0, [Math]::Min($buffer.Length, 8192 - $total))
            if ($read -gt 0) {
                $total += $read
                $safeText = [Text.Encoding]::UTF8.GetString($buffer, 0, $read)
                $safeText = $safeText -replace '(?i)(password|passwd|token|api[_ -]?key|ssid)\s*[:=]\s*\S+', '$1=[REDACTED]'
                $safeText = $safeText -replace '\b(?:\d{1,3}\.){3}\d{1,3}\b', '[IP]'
                $safeText = $safeText -replace '\b(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}\b', '[MAC]'
                Write-Output $safeText
            }
        } catch [TimeoutException] {
            continue
        }
    }
    Write-Host "Received $total bytes. Raw output is not saved."
} finally {
    if ($serial.IsOpen) { $serial.Close() }
    $serial.Dispose()
}
