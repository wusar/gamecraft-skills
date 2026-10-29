param([string]$Voice = 'Microsoft Huihui Desktop')
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
$board = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'storyboard.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$audioRoot = Join-Path $PSScriptRoot 'output/audio'
New-Item -ItemType Directory -Path $audioRoot -Force | Out-Null
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
try {
 $synth.SelectVoice($Voice)
 $synth.Rate = 1
 foreach ($scene in $board.scenes) {
  $phrases = [regex]::Matches($scene.narration, '[^。！？]+[。！？]?')
  for ($index = 0; $index -lt $phrases.Count; $index++) {
   $audioPath = Join-Path $audioRoot ('{0}-{1:D2}.wav' -f $scene.id, $index)
   if (Test-Path -LiteralPath $audioPath) { continue }
   $synth.SetOutputToWaveFile($audioPath)
   $synth.Speak($phrases[$index].Value)
   $synth.SetOutputToNull()
  }
  Write-Output ('Narrated: ' + $scene.id)
 }
} finally { $synth.Dispose() }
