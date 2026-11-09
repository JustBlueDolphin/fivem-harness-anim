from pathlib import Path
import xml.etree.ElementTree as ET
from lupa import LuaRuntime
ROOT=Path(__file__).parent;RESOURCE=ROOT.parent
lua=LuaRuntime(unpack_returned_tuples=True)
lua.execute('''
registered={};commands={};handlers={};threads={};messages={};events={};now=1000
ped=1;vehicle=10;class=0;occupant=1;seat=-1;seatX=-.35;inside=true;dead=false;loaded=true;playing=true;ragdoll=false
flags={[1]=true};missing=false;driveby=false
function exports(n,f) registered[n]=f end
function RegisterCommand(n,f) commands[n]=f end
function RegisterKeyMapping(...) mapped=table.pack(...) end
function AddEventHandler(n,f) handlers[n]=f end
function CreateThread(f) local t=coroutine.create(f);table.insert(threads,t);return t end
function Wait(ms) coroutine.yield(ms) end
function PlayerPedId() return ped end
function IsEntityDead() return dead end
function IsPedInAnyVehicle() return inside end
function GetVehiclePedIsIn() return vehicle end
function GetEntitySpeed() return speed or 0 end
function GetEntityModel() return 99 end
function GetVehicleClass() return class end
function GetVehicleMaxNumberOfPassengers() return 3 end
function GetPedInVehicleSeat(_,index) return index==seat and occupant or 0 end
function GetEntityCoords() return {x=seatX,y=0,z=0} end
function GetOffsetFromEntityGivenWorldCoords(_,x,y,z) return {x=x,y=y,z=z} end
function DoesEntityExist() return true end
function IsPedRagdoll() return ragdoll end
function IsPedDoingDriveby() return driveby end
function GetGameTimer() return now end
function HasAnimDictLoaded() return loaded end
function RequestAnimDict() requested=true end
function GetAnimDuration() return missing and 0 or 2.4 end
function TaskPlayAnim(...) call=table.pack(...) end
function StopAnimTask() stopped=true end
function IsEntityPlayingAnim() return playing end
function GetPedConfigFlag(p) return flags[p] end
function SetPedConfigFlag(p,_,v) flags[p]=v end
function DisableControlAction(_,control) blocked=control end
function GetCurrentResourceName() return 'harness_anim' end
function RemoveAnimDict() removed=true end
function TriggerEvent(name,...)
 if name=='chat:addMessage' then table.insert(messages,({...})[1].args[2])
 else table.insert(events,table.pack(name,...)) end
end
function step(t,delta) now=now+(delta or 0);local ok,e=coroutine.resume(t);assert(ok,e) end
function finish(t) while coroutine.status(t)~='dead' do step(t,100) end end
''')
for f in ['config.lua','client.lua','fxmanifest.lua']:
    text=(RESOURCE/f).read_text()
    assert lua.eval('function(s) return load(s)~=nil end')(text),f
    if f!='fxmanifest.lua':lua.execute(text)
lua.execute('''
assert(mapped[4]=='K')
speed=2;local ok,reason=registered.Toggle();assert(not ok and reason=='vehicle_moving');speed=0
assert(not registered.IsBuckled())
assert(registered.Toggle());assert(registered.IsBusy())
local ok,reason=registered.Toggle();assert(not ok and reason=='busy')
local t=threads[#threads];step(t)
assert(call[3]=='harness_fasten' and call[8]==0 and call[10]==2)
finish(t);assert(registered.IsBuckled());assert(flags[1]==false)
step(threads[1]);assert(blocked==75)
assert(registered.SetBuckled(false));t=threads[#threads];step(t)
assert(call[3]=='harness_release');finish(t);assert(not registered.IsBuckled());assert(flags[1]==true)
-- Right-side passenger uses opposite arm and cleanup restores the prior flag value.
seat=0;seatX=.35;flags[1]=false
assert(registered.Toggle());t=threads[#threads];step(t);assert(call[3]=='harness_fasten');finish(t)
inside=false;assert(not registered.IsBuckled());assert(flags[1]==false)
-- Unavailable clips/tasks and a changing context never falsely buckle the player.
inside=true;seat=-1;seatX=-.35;playing=false
assert(registered.Toggle());finish(threads[#threads]);assert(not registered.IsBuckled())
playing=true;missing=true
assert(registered.Toggle());finish(threads[#threads]);assert(not registered.IsBuckled())
missing=false;loaded=false
assert(registered.Toggle());t=threads[#threads];step(t);assert(requested)
vehicle=11;step(t,100);assert(not registered.IsBusy() and not registered.IsBuckled())
loaded=true;flags[1]=true
assert(registered.Toggle());finish(threads[#threads]);assert(registered.IsBuckled())
-- Cancelling an unbuckle gesture while still seated preserves the fastened state.
assert(registered.Toggle());t=threads[#threads];step(t);driveby=true;step(t,100)
assert(registered.IsBuckled());driveby=false
-- Seat changes and ped replacement clear the bound state, restoring old ped flags.
seat=0;assert(not registered.IsBuckled());assert(flags[1]==true)
seat=-1;assert(registered.Toggle());finish(threads[#threads])
ped=2;occupant=2;assert(not registered.IsBuckled());assert(flags[1]==true)
class=8;assert(not registered.Toggle());class=0
flags[2]=true;assert(registered.Toggle());finish(threads[#threads]);assert(flags[2]==false)
handlers.onResourceStop('harness_anim');assert(flags[2]==true and removed)
''')

print('PASS: harness toggle lifecycle, missing/interrupted playback, seat/ped changes, prior flag restoration and cleanup')
