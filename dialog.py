import subprocess


def run_cmd(cmd):
	results = subprocess.check_output(cmd).decode("utf-8")
	return results


def osascript_wrapper(cmd):
	return ["osascript", "-e", cmd]


def popup_multipicker(title, message, options):
	options_string = '"' + "\", \"".join(options) + '"'
	cmd = "choose from list {" + options_string + "} with title \"" + title + "\" with prompt \"" + message + "\" default items \"" + options[0] +"\" with multiple selections allowed"
	cmd = osascript_wrapper(cmd)
	return run_cmd(cmd)


def send_to_clipboard(w):
	cmd = "set the clipboard to \"" + w.strip() +"\""
	cmd = osascript_wrapper(cmd)
	run_cmd(cmd)


def get_tmux_buffers():
	bufs = run_cmd("tmux list-buffers".split())
	buffers = []
	for buf in bufs.split('\n'):
		text = buf.strip().split("bytes:")
		if len(text) > 1:
			buffers.append(text[1].strip()[1:-1])
	return buffers


def main():
	options = get_tmux_buffers()
	if len(options) > 0:
		result = popup_multipicker("Tmux selector", "Select a buffer:", options)
		send_to_clipboard(result)


if __name__ == "__main__":
	main()
