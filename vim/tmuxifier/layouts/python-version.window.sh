# Set window root path. Default is `$session_root`.
# Must be called before `new_window`.
window_root "~/projects/python-version"

# Create new window. If no argument is given, window name will be based on
# layout file name.
new_window "python-version"

# Split window into panes.
split_h 60
select_pane 0
split_v 50
select_pane 2
split_v 60

# Run commands.
#run_cmd "top"     # runs in active pane
run_cmd "conda activate py39" 0
run_cmd "./task test:watch" 0

run_cmd "conda activate py39" 1
run_cmd "lazygit" 1

run_cmd "conda activate py39" 2
run_cmd "vi test_version.py" 2

run_cmd "conda activate py39" 3
run_cmd "vi version.py" 3

# Paste text
#send_keys "top"    # paste into active pane
#send_keys "date" 1 # paste into pane 1

# Set active pane.
select_pane 4

