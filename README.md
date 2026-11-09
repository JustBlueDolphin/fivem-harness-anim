# Five-point harness animations

**Made with AI** — the custom animations and FiveM client script were created with AI assistance.

Standalone resource with the approved smoother harness fastening (8.6 seconds) and centre-buckle release (3.8 seconds). Arm movements only; no visible harness straps. Includes a toggle for drivers and passengers.

[Watch the animations](previews/harness-review-v2.mp4)

## Install and use

Copy `harness_anim` into your server resources. Add this to `server.cfg`:

```cfg
ensure harness_anim
```

For a running server, run `refresh` then `ensure harness_anim`. Press **K** or type `/harness`. The key can be remapped in FiveM settings. `/harness on`, `/harness off` and `/harness status` are also available.

Both hands leave the wheel, so fastening/releasing requires speed at or below 1 m/s by default. Change `Config.MaxToggleSpeed` or set it to `false` to remove that check. The animation and new harness state complete together; loading failures, failed tasks or interrupted gestures do not commit the new state. A second toggle during a gesture is rejected.

While fastened, the script blocks the vehicle-exit control and optionally disables GTA's built-in windscreen-ejection flag. It captures and restores the original flag on release, vehicle/seat/ped changes, death or resource stop. This is not custom crash protection or a damage-reduction system. It does not override another script's independent ejection logic.

Supported classes: cars, SUVs, vans, trucks, buses and open-wheel vehicles. Bikes, boats, aircraft and trains are excluded. `Config.Models[joaat('model')] = false` excludes an individual model. Both hands animate, so the same clips are used for either seating side.

## Integration

```lua
exports['harness_anim']:Toggle()
exports['harness_anim']:SetBuckled(true)
local fastened = exports['harness_anim']:IsBuckled()
local busy = exports['harness_anim']:IsBusy()
AddEventHandler('harness_anim:changed', function(fastened, vehicle)
    -- Update your HUD here.
end)
```

`Toggle` / `SetBuckled` return `true, 'started'` when loading begins, not when fastening finishes. The change event signals completion. Use one restraint implementation at a time: separate seatbelt scripts can conflict over exit controls and ped flags. Other secondary animations can interrupt the gesture; test parked and use `/gearshift off` if needed.

## Validation and credits

The two native YCD clips were saved/reloaded with CodeWalker. Preview poses, endpoint matching and sampled joint continuity were checked. Offline Lua tests cover state changes, passengers, failures, speed checks and cleanup (`pip install lupa`, then `python tests/test_client.py`). Actual FiveM playback, MP female positioning and arbitrary vehicle interiors remain unverified. Version 0.1.0 is a prerelease for in-game testing.

The preview uses Rockstar Games' MP male ped and Sultan reference models. The dashboard and steering wheel are hidden in the preview to expose the fastening area. Those third-party models are not AI-created assets and are not included as streamed game assets. The custom animation and script are the AI-assisted work.
