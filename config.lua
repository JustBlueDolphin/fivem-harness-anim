Config = {}
Config.Dictionary = 'harness'
Config.Command = 'harness'
Config.Key = 'K'
Config.LoadTimeoutMs = 10000
Config.Durations = { buckle = 8600, unbuckle = 3800 }
Config.BlockExit = true
Config.DisableWindscreenEjection = true
Config.EnabledClasses = { [0]=true,[1]=true,[2]=true,[3]=true,[4]=true,[5]=true,
    [6]=true,[7]=true,[9]=true,[10]=true,[11]=true,[12]=true,[17]=true,
    [18]=true,[19]=true,[20]=true,[22]=true }
-- Per-model exclusions or seat-side overrides for unusual vehicle interiors.
Config.Models = {
    -- [joaat('my_car')] = false,
    -- [joaat('my_car')] = { side = 'left' }, -- 'left'/'right' seating side
}

-- Both hands leave the wheel; set false to allow toggling at any speed.
Config.MaxToggleSpeed = 1.0 -- metres/second
