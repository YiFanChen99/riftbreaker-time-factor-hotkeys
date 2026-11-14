# riftbreaker-time-factor-hotkeys

The Riftbreaker 的本機 mod：用熱鍵切換遊戲速度，不必每次打開 console 輸入 `time_factor`。

## 功能

在任務中按下熱鍵，就會執行對應的 console 指令 `time_factor <倍率>`：

| 按鍵 | 指令 | 效果 |
|---|---|---|
| F1 | `time_factor 0.3` | 慢速 |
| F2 | `time_factor 1` | 正常速度 |
| F3 | `time_factor 1.5` | 1.5 倍速 |
| F4 | `time_factor 3` | 3 倍速 |

- 按鍵和倍率都可以自訂，改完重開遊戲生效。
- 預設的 F1～F4 沒有和遊戲內建按鍵衝突（F5 快速存檔、F8 快速讀檔、F11 debug 選單）。
- 切換的速度不會寫進遊戲設定檔（`user.cfg`、`local.cfg`）。
- 只在單人遊戲測試過。多人連線時 `time_factor` 的行為未經測試。

## 使用方式

需要 Python 3。

```sh
python install.py                  # 安裝；改過檔案後也用這個重新安裝
python install.py save-manifest    # 發佈到 Workshop 後，把含 Workshop ID 的 manifest 存回本專案
python install.py remove           # 移除
```

遊戲不在預設路徑 `D:\SteamLibrary\steamapps\common\Riftbreaker` 時，加上 `--game-dir <遊戲資料夾>`。

安裝後直接開遊戲、進任務就能用，不需要在遊戲裡啟用。

### 改熱鍵

修改 [`lua/time_factor_hotkeys_autoexec.lua`](lua/time_factor_hotkeys_autoexec.lua) 開頭的 `SPEED_KEYS`，再執行 `python install.py`，然後重開遊戲：

```lua
local SPEED_KEYS = {
    { key = "f1", time_factor = "0.3" },
    { key = "f2", time_factor = "1" },
    { key = "f3", time_factor = "1.5" },
    { key = "f4", time_factor = "3" },
}
```

- 可以增減列數，`time_factor` 填任意倍率。
- 按鍵名稱是小寫的引擎按鍵名，例如 `f1`、`lcontrol`、`ml`（滑鼠左鍵）。完整列表見 [EXOR 官方 wiki 的按鍵表](https://exorstudios.github.io/riftbreaker-wiki/docs/modding-files/lua-files/accessing-keyboard-hotkeys/)；實測過的只有 `f1`～`f4`。
- 也可以直接改已安裝的那份 `<遊戲資料夾>\mods\time_factor_hotkeys\lua\time_factor_hotkeys_autoexec.lua`，不必重新安裝。但下次執行 `install.py` 會被專案裡的版本蓋掉。

## 介面

| 介面 | 位置 | 用途 |
|---|---|---|
| 遊戲內熱鍵 | F1～F4（預設） | 切換 `time_factor` |
| `SPEED_KEYS` 設定表 | `lua/time_factor_hotkeys_autoexec.lua` 開頭 | 定義按鍵與倍率 |
| `install.py` | 專案根目錄 | 安裝、重新安裝、存回 manifest（`save-manifest`）、移除（`remove`），可用 `--game-dir` 指定遊戲資料夾 |
| `time_factor_hotkeys.manifest` | 專案根目錄 | mod 的標題、說明、標籤、版本，以及發佈後的 Workshop ID（`steam_published_file`） |
| `time_factor_hotkeys.png` | 專案根目錄 | Workshop 預覽圖 |
| `changelog.txt` | 專案根目錄 | 發佈時當作 Steam 的更新說明 |
| 遊戲 log | `文件\The Riftbreaker\exor_logs.txt` | 每次載入地圖會記錄 `[time_factor_hotkeys] bound f1 to time_factor 0.3` 這類訊息，用來確認 mod 有生效 |

## 運作方式

- 遊戲會載入 `<遊戲資料夾>\mods\` 底下的本機 mod。
- `lua/` 裡檔名以 `_autoexec.lua` 結尾的檔案，每次建立地圖時都會自動執行。
- 這個腳本用引擎的 `bind` 指令，把按鍵綁到 console 指令：`ConsoleService:ExecuteCommand('bind f4 "time_factor 3"')`。

本機 mod 必須是**資料夾**，裡面放同名的 `.manifest`，遊戲才讀得到它的版本。做成 zip 的話，manifest 不會被讀取，開遊戲時會跳出「不相容的模組」提示，版本顯示「Unknown」。

設定選單裡的「控制設定」清單寫死在遊戲主程式中，mod 無法把這些熱鍵加進去，所以改鍵要改 Lua 檔。

## 發佈到 Steam Workshop

`<遊戲資料夾>\mods\` 底下的每個資料夾，同時也是官方 Workspace Editor 的 workspace，所以安裝好的 `mods\time_factor_hotkeys\` 可以直接發佈。

1. 在 Steam 收藏庫勾選「工具」篩選，安裝 **The Riftbreaker - Tools**（約 1 GB，裝在 `<遊戲資料夾>\tools\`）。
2. 執行 `python install.py`，確保 workspace 是最新的。
3. 開啟 `<遊戲資料夾>\tools\bin\workspace_editor_win_release.exe`，選擇 `time_factor_hotkeys` workspace。
4. 用 **Update workspace manifest** 確認標題、說明、標籤、可見度（Public / Private）和預覽圖。
5. 按 **Publish**，選 Steam。Steam 必須是「線上」狀態。
6. 第一次發佈時，Steam 可能要求接受 Workshop 法律協議，項目才會公開顯示。
7. 執行 `python install.py save-manifest`，把含 Workshop ID 的 manifest 存回本專案，然後 commit。

之後要更新：修改 `changelog.txt` 和 manifest 的 `version`，再重複第 2～5、7 步。

- **Workshop ID 不能弄丟**：manifest 的 `steam_published_file` 是 `0` 時，Publish 會建立一個新的 Workshop 項目，而不是更新原本那個。`install.py` 不會覆蓋 workspace 裡既有的 manifest。`remove` 發現 workspace 的 ID 還沒存回本專案時，也會拒絕刪除。
- **預覽圖規格**（編輯器的檢查條件）：PNG、16:9、至少 512×288、不超過 2 MB，檔名是 `<workspace 名稱>.png`。
- **可選標籤**：Buildings、Creatures、Items、Missions、Mod Pack、Other、Rebalance、Research、Skins、Tiles、Weapons。
- 自己訂閱測試時，記得在 Workspace Editor 停用本機的 workspace，避免同一個 mod 被載入兩次。

以上流程是從 Workspace Editor 程式內的文字和 Steam API 呼叫整理出來的，還沒有實際發佈過。

## 改了哪些東西

安裝時只會**新增**這個資料夾，不修改任何遊戲原檔或玩家設定：

```
<遊戲資料夾>\mods\time_factor_hotkeys\
├─ time_factor_hotkeys.manifest            ← 只在不存在時從本專案複製，之後保留（發佈會寫入 Workshop ID）
├─ time_factor_hotkeys.png                 ← Workshop 預覽圖，每次安裝都更新
├─ changelog.txt                           ← 更新說明，每次安裝都更新
└─ lua\time_factor_hotkeys_autoexec.lua    ← 每次安裝都更新
```

- 第一次安裝時，如果 `<遊戲資料夾>\mods\` 不存在，會建立它。遊戲自己也會在裡面建立 `mods_disabled.txt`，記錄你在遊戲裡停用的本機 mod。
- 沒有修改：遊戲安裝檔（`packs\`、`bin\`）、`user.cfg`、`local.cfg`、按鍵設定檔（`*.am`）。
- `python install.py remove` 會刪除整個 `mods\time_factor_hotkeys\` 資料夾，回到安裝前的狀態（`mods\` 資料夾本身和 `mods_disabled.txt` 會保留）。如果 workspace 的 manifest 有本專案還沒存回的 Workshop ID，會先拒絕刪除。
