on open (files_to_open)
	if length of files_to_open is equal to 0 then
		tell application "Terminal"
			activate
			do script "unset HISTFILE; echo -en '\\033[8;48;132t'; vim; exit"
		end tell
	else
		tell application "Terminal"
			activate
			do script "unset HISTFILE; echo -en '\\033[8;48;132t'; vim " & quoted form of POSIX path of item 1 of files_to_open & "; exit"
		end tell
		if length of files_to_open is greater than 1 then
			repeat with i from 2 to length of files_to_open
				tell application "System Events"
					tell process "Terminal"
						keystroke "t" using command down
					end tell
				end tell
				tell application "Terminal"
					do script "unset HISTFILE; echo -en '\\033[8;48;132t'; vim " & quoted form of POSIX path of item i of files_to_open & "; exit" in selected tab of the front window
				end tell
			end repeat
		end if
	end if
end open