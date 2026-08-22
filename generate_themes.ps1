param(
    [string]$ProjectRoot = $PSScriptRoot,
    [switch]$ValidateOnly,
    [switch]$RepairFrames,
    [switch]$RegenerateThemeDigits
)

Add-Type -AssemblyName System.Drawing

$defaultRoot = Join-Path $ProjectRoot 'resources/default'
$themesRoot = Join-Path $ProjectRoot 'resources'
$themeSpecs = @(
    @{ Key = 'candy_kingdom'; Wall = [Drawing.Color]::FromArgb(255, 245, 190); Sky = [Drawing.Color]::FromArgb(255, 182, 220); Accent = [Drawing.Color]::FromArgb(235, 92, 145); Enemies = @(
        @{ Name = 'marshmallow_man'; Primary = [Drawing.Color]::White; Secondary = [Drawing.Color]::FromArgb(235, 170, 190); Death = 'melt' },
        @{ Name = 'springfield_doughnut'; Primary = [Drawing.Color]::FromArgb(235, 150, 180); Secondary = [Drawing.Color]::FromArgb(120, 75, 45); Death = 'crumble' },
        @{ Name = 'gingerbread_golem'; Primary = [Drawing.Color]::FromArgb(165, 95, 48); Secondary = [Drawing.Color]::FromArgb(255, 220, 120); Death = 'crumble' }
    ) },
    @{ Key = 'space'; Wall = [Drawing.Color]::FromArgb(35, 55, 95); Sky = [Drawing.Color]::FromArgb(8, 12, 35); Accent = [Drawing.Color]::FromArgb(70, 220, 255); Enemies = @(
        @{ Name = 'alien_drone'; Primary = [Drawing.Color]::FromArgb(75, 210, 180); Secondary = [Drawing.Color]::FromArgb(25, 90, 110); Death = 'burst' },
        @{ Name = 'alien_warrior'; Primary = [Drawing.Color]::FromArgb(115, 170, 240); Secondary = [Drawing.Color]::FromArgb(40, 55, 125); Death = 'burst' },
        @{ Name = 'alien_overlord'; Primary = [Drawing.Color]::FromArgb(190, 100, 245); Secondary = [Drawing.Color]::FromArgb(75, 25, 125); Death = 'burst' }
    ) },
    @{ Key = 'graveyard'; Wall = [Drawing.Color]::FromArgb(65, 75, 75); Sky = [Drawing.Color]::FromArgb(20, 27, 42); Accent = [Drawing.Color]::FromArgb(155, 220, 190); Enemies = @(
        @{ Name = 'ghost'; Primary = [Drawing.Color]::FromArgb(210, 235, 225); Secondary = [Drawing.Color]::FromArgb(125, 180, 175); Death = 'fade' },
        @{ Name = 'vampire'; Primary = [Drawing.Color]::FromArgb(150, 35, 65); Secondary = [Drawing.Color]::FromArgb(35, 25, 55); Death = 'dust' },
        @{ Name = 'werewolf'; Primary = [Drawing.Color]::FromArgb(125, 105, 90); Secondary = [Drawing.Color]::FromArgb(55, 45, 45); Death = 'dust' }
    ) }
)

function New-Canvas([int]$Size = 96) {
    $bitmap = New-Object Drawing.Bitmap($Size, $Size)
    $graphics = [Drawing.Graphics]::FromImage($bitmap)
    $graphics.SmoothingMode = [Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $graphics.Clear([Drawing.Color]::Transparent)
    return @{ Bitmap = $bitmap; Graphics = $graphics }
}

function Save-Frame($Canvas, [string]$Path) {
    $Canvas.Graphics.Dispose()
    $Canvas.Bitmap.Save($Path, [Drawing.Imaging.ImageFormat]::Png)
    $Canvas.Bitmap.Dispose()
}

function New-EnemyFrame($Enemy, [string]$Animation, [int]$Frame, [string]$Path) {
    $canvas = New-Canvas
    $g = $canvas.Graphics
    $primary = New-Object Drawing.SolidBrush($Enemy.Primary)
    $secondary = New-Object Drawing.SolidBrush($Enemy.Secondary)
    $outline = New-Object Drawing.Pen([Drawing.Color]::FromArgb(45, 30, 55), 3)
    $offset = [int](($Frame - 1.5) * 2)
    $deathProgress = if ($Animation -eq 'death') { $Frame / 5 } else { 0 }
    if ($Animation -eq 'death' -and $Enemy.Death -eq 'melt') {
        $g.FillEllipse($primary, 20, 62 + [int]($deathProgress * 12), 56, 18)
        $g.FillEllipse($secondary, 28, 54 + [int]($deathProgress * 10), 10, 20)
    } elseif ($Animation -eq 'death' -and $Enemy.Death -eq 'crumble') {
        for ($piece = 0; $piece -lt 7; $piece++) { $g.FillRectangle($primary, 20 + (($piece * 17 + $Frame * 5) % 55), 25 + (($piece * 13 + $Frame * 9) % 55), 9, 9) }
        $g.FillEllipse($secondary, 35, 42 + $Frame * 3, 10, 7)
    } elseif ($Animation -eq 'death') {
        $alpha = [Math]::Max(35, 255 - ($Frame * 38))
        $fade = New-Object Drawing.SolidBrush([Drawing.Color]::FromArgb($alpha, $Enemy.Primary.R, $Enemy.Primary.G, $Enemy.Primary.B))
        $g.FillEllipse($fade, 22, 22 + $Frame * 3, 52, 52)
        $fade.Dispose()
    } else {
        $g.FillEllipse($primary, 22 + $offset, 18, 52, 60)
        $g.FillEllipse($secondary, 31 + $offset, 29, 12, 12)
        $g.FillEllipse($secondary, 53 + $offset, 29, 12, 12)
        $g.DrawEllipse($outline, 22 + $offset, 18, 52, 60)
        if ($Animation -eq 'attack') { $g.FillRectangle($secondary, 40, 63, 18, 18) }
        if ($Animation -eq 'pain') { $g.DrawLine($outline, 25, 24, 68, 67) }
        if ($Animation -eq 'walk') { $g.FillRectangle($secondary, 30 + $offset, 73, 12, 15); $g.FillRectangle($secondary, 54 - $offset, 73, 12, 15) }
    }
    $primary.Dispose(); $secondary.Dispose(); $outline.Dispose()
    Save-Frame $canvas $Path
}

function New-PercentTexture($Theme, [string]$Path) {
    $canvas = New-Canvas 64
    $g = $canvas.Graphics
    $font = [Drawing.Font]::new('Arial', 54, [Drawing.FontStyle]::Bold)
    $shadow = New-Object Drawing.SolidBrush([Drawing.Color]::FromArgb(120, 20, 20, 20))
    $accent = New-Object Drawing.SolidBrush($Theme.Accent)
    $glyphSize = $g.MeasureString('%', $font)
    $glyphX = [int]((64 - $glyphSize.Width) / 2)
    $glyphY = [int]((64 - $glyphSize.Height) / 2 - 3)
    $g.DrawString('%', $font, $shadow, $glyphX + 2, $glyphY + 2)
    $g.DrawString('%', $font, $accent, $glyphX, $glyphY)
    $font.Dispose()
    $shadow.Dispose()
    $accent.Dispose()
    Save-Frame $canvas $Path
}

$animationMinimums = @{ idle = 1; attack = 2; pain = 2; walk = 4; death = 6 }

function Repair-AnimationFrames($Enemy, [string]$Animation, [string]$AnimationRoot, [int]$MinimumFrames, [bool]$AllowRepair) {
    New-Item $AnimationRoot -ItemType Directory -Force | Out-Null
    for ($frame = 0; $frame -lt $MinimumFrames; $frame++) {
        $framePath = Join-Path $AnimationRoot "$frame.png"
        if (-not (Test-Path $framePath) -and $AllowRepair) {
            New-EnemyFrame $Enemy $Animation $frame $framePath
            Write-Host "Generated missing $Animation frame: $framePath"
        } elseif (-not (Test-Path $framePath)) {
            Write-Host "Missing $Animation frame detected: $framePath"
        }
    }

    $hashes = @{}
    foreach ($frameFile in Get-ChildItem $AnimationRoot -Filter '*.png' | Sort-Object Name) {
        $hash = (Get-FileHash $frameFile.FullName -Algorithm SHA256).Hash
        if ($hashes.ContainsKey($hash)) {
            $match = [regex]::Match($frameFile.BaseName, '\d+$')
            if ($match.Success -and $AllowRepair) {
                $frameNumber = [int]$match.Value
                New-EnemyFrame $Enemy $Animation $frameNumber $frameFile.FullName
                Write-Host "Regenerated duplicate $Animation frame: $($frameFile.FullName)"
            } elseif ($match.Success) {
                Write-Host "Duplicate $Animation frame detected: $($frameFile.FullName)"
            }
        } else {
            $hashes[$hash] = $frameFile.FullName
        }
    }
}

if ($RegenerateThemeDigits) {
    foreach ($theme in $themeSpecs) {
        $themeRoot = Join-Path $themesRoot $theme.Key
        New-Item (Join-Path $themeRoot 'textures/digits') -ItemType Directory -Force | Out-Null
        New-PercentTexture $theme (Join-Path $themeRoot 'textures/digits/10.png')
        Write-Host "Generated themed percent texture: $themeRoot/textures/digits/10.png"
    }
}

if (-not $ValidateOnly -and -not $RegenerateThemeDigits) {
foreach ($theme in $themeSpecs) {
    $themeRoot = Join-Path $themesRoot $theme.Key
    Copy-Item (Join-Path $defaultRoot 'sound') (Join-Path $themeRoot 'sound') -Recurse -Force
    Copy-Item (Join-Path $defaultRoot 'sprites/animated_sprites') (Join-Path $themeRoot 'sprites/animated_sprites') -Recurse -Force
    Copy-Item (Join-Path $defaultRoot 'sprites/static_sprites') (Join-Path $themeRoot 'sprites/static_sprites') -Recurse -Force
    Copy-Item (Join-Path $defaultRoot 'sprites/weapon') (Join-Path $themeRoot 'sprites/weapon') -Recurse -Force
    New-Item (Join-Path $themeRoot 'textures/digits') -ItemType Directory -Force | Out-Null
    foreach ($file in Get-ChildItem (Join-Path $defaultRoot 'textures/digits')) { Copy-Item $file.FullName (Join-Path $themeRoot 'textures/digits') -Force }
    New-PercentTexture $theme (Join-Path $themeRoot 'textures/digits/10.png')
    New-Item (Join-Path $themeRoot 'textures') -ItemType Directory -Force | Out-Null
    foreach ($name in @('blood_screen.png', 'game_over.png', 'win.png')) { Copy-Item (Join-Path $defaultRoot "textures/$name") (Join-Path $themeRoot 'textures') -Force }

    $wallCanvas = New-Canvas 256; $wallCanvas.Graphics.Clear($theme.Wall); $wallCanvas.Graphics.DrawRectangle((New-Object Drawing.Pen($theme.Accent, 8)), 8, 8, 240, 240); Save-Frame $wallCanvas (Join-Path $themeRoot 'textures/1.png')
    Copy-Item (Join-Path $themeRoot 'textures/1.png') (Join-Path $themeRoot 'textures/2.png') -Force
    Copy-Item (Join-Path $themeRoot 'textures/1.png') (Join-Path $themeRoot 'textures/3.png') -Force
    Copy-Item (Join-Path $themeRoot 'textures/1.png') (Join-Path $themeRoot 'textures/4.png') -Force
    Copy-Item (Join-Path $themeRoot 'textures/1.png') (Join-Path $themeRoot 'textures/5.png') -Force
    $skyCanvas = New-Canvas 256; $skyCanvas.Graphics.Clear($theme.Sky); Save-Frame $skyCanvas (Join-Path $themeRoot 'textures/sky.png')

    foreach ($enemy in $theme.Enemies) {
        foreach ($animation in @('idle', 'walk', 'attack', 'pain', 'death')) {
            $animationRoot = Join-Path $themeRoot "sprites/npc/$($enemy.Name)/$animation"
            New-Item $animationRoot -ItemType Directory -Force | Out-Null
            $count = if ($animation -eq 'pain') { 2 } elseif ($animation -eq 'death') { 6 } else { 4 }
            for ($frame = 0; $frame -lt $count; $frame++) { New-EnemyFrame $enemy $animation $frame (Join-Path $animationRoot "$frame.png") }
        }
        New-EnemyFrame $enemy 'idle' 0 (Join-Path $themeRoot "sprites/npc/$($enemy.Name)/0.png")
    }
}
}

foreach ($theme in $themeSpecs) {
    foreach ($enemy in $theme.Enemies) {
        foreach ($animation in $animationMinimums.Keys) {
            $animationRoot = Join-Path $themesRoot "$($theme.Key)/sprites/npc/$($enemy.Name)/$animation"
                $allowRepair = $RepairFrames -and $theme.Key -ne 'candy_kingdom'
                Repair-AnimationFrames $enemy $animation $animationRoot $animationMinimums[$animation] $allowRepair
        }
    }
}

if ($RepairFrames) {
    Write-Host 'Validated and repaired theme animation assets.'
} elseif ($ValidateOnly) {
    Write-Host 'Validated theme animation assets without modifying artwork.'
} else {
    Write-Host 'Generated and validated Candy Kingdom, Space, and Graveyard theme assets.'
}