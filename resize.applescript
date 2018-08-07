on run argv
	set a to item 1 of argv
	set w to item 2 of argv
	set h to item 3 of argv
	tell application a
		activate
		reopen
		set the bounds of the first window to {0, 0, w, h}
	end tell
end run