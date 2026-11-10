-- Time Factor Hotkeys
-- Binds keys to the console command `time_factor <value>` each time a map is created.
-- To change a key, edit SPEED_KEYS, run `python install.py` again, then restart the game.
-- Editing the installed copy in <game dir>/mods/time_factor_hotkeys/lua/ also works,
-- but the next `python install.py` overwrites it with this file.
-- Key names are the engine's lowercase key names, such as f1, lcontrol or ml (left mouse); see
-- https://exorstudios.github.io/riftbreaker-wiki/docs/modding-files/lua-files/accessing-keyboard-hotkeys/

local SPEED_KEYS = {
    { key = "f1", time_factor = "0.3" },
    { key = "f2", time_factor = "1" },
    { key = "f3", time_factor = "1.5" },
    { key = "f4", time_factor = "3" },
}

for _, binding in ipairs( SPEED_KEYS ) do
    ConsoleService:ExecuteCommand( 'bind ' .. binding.key .. ' "time_factor ' .. binding.time_factor .. '"' )
    LogService:Log( "[time_factor_hotkeys] bound " .. binding.key .. " to time_factor " .. binding.time_factor )
end
