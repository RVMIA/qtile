# Qtile config.py
from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.command import lazy
import subprocess
import os
import re



@hook.subscribe.startup_once
def autostart():
    subprocess.Popen([os.path.expanduser('~/.config/autostart.sh')])
    subprocess.Popen([os.path.expanduser('~/.config/wlrrandr.sh')])
    processes = [
        ["spotify"],
        ["discord"]
    ]
    for p in processes:
        subprocess.Popen(p)

@hook.subscribe.focus_change
def _():
    for window in qtile.current_group.windows:
        if window.floating:
            window.cmd_bring_to_front()


@hook.subscribe.client_managed
def auto_show_screen(window):
    # check whether group is visible on any screen right now
    # qtile.groups_map['<somegroup>'].screen is None in case it is currently not shown on any screen
    visible_groups = [group_name for group_name, group in qtile.groups_map.items() if group.screen]

    if window.group.name not in visible_groups:
        window.group.cmd_toscreen()



        
mod = "mod4"
terminal = "kitty"

keys = [
    ### WINDOWING KEYS
    
    # https://github.com/qtile/qtile/blob/master/docs/manual/config/lazy.rst
    # Switch between windows
    Key([mod], "j", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "i", lazy.layout.up()),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "j", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "i", lazy.layout.shuffle_up()),
    Key([mod], "tab", lazy.layout.next()),     # like alt tab

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "j", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod, "control"], "k", lazy.layout.grow_down()),
    Key([mod, "control"], "i", lazy.layout.grow_up()),
    Key([mod], "n", lazy.layout.normalize()),

    # Toggle between different layouts as defined below
    Key([mod], "space", lazy.next_layout()),
    Key([mod, "shift"], "c", lazy.window.kill()),
    Key([mod], "q", lazy.reload_config()),
    Key([mod, "shift"], "q", lazy.shutdown()),
    Key([mod], "t", lazy.window.toggle_floating()),
    
    ###


    ### SPAWN COMMANDS
    Key([mod, "shift"], "Return", lazy.spawn(terminal)),
    Key([mod], "f", lazy.spawn("librewolf")),
    Key([mod, "shift"], "e", lazy.spawn("emacsclient -c -a emacs")),
    Key([mod, "shift"], "p", lazy.spawn("spotify")),
    Key([mod, "shift"], "d", lazy.spawn("discord")),
    Key([mod], "p", lazy.spawn("bash /home/ame/.config/wal/dmen.sh")),
    Key([mod, "shift"], "t", lazy.spawn("thunar")),
    Key([mod, "shift"], "delete", lazy.spawn("slock")),
    Key([mod, "shift"], "s", lazy.spawn("/home/ame/.config/scripts/screenshot.sh")),

    Key([], "XF86AudioPlay", lazy.spawn("playerctl -p spotify play-pause")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl -p spotify previous")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl -p spotify next")),

]

# https://pastebin.com/aU7in33p # Line 97
groups = [
    Group("1"),
    Group("2"),
    Group("3"),
    Group("4"),
    Group("5"),
    Group("6"),
    Group("7"),
    Group("8"),
    Group("9", layout = "bsp", matches = [Match(wm_class = ["Spotify","discord"])]),
]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            # mod1 + shift + letter of group = move focused window to group
            Key([mod], i.name, lazy.group[i.name].toscreen()),
            Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
        ]
    )

layout_theme = {
    "margin": 10,
    "border_focus":"df5412",
    "border_normal":"0f0f0f",
    "border_focus_stack":"df5714",
    "border_width": 4
}

layouts = [
    #layout.Columns(**layout_theme),
    #layout.Stack(**layout_theme),
    layout.Max(**layout_theme),
    layout.Bsp(**layout_theme),
  ]

widget_defaults = dict(
    font="Iosevka",
    fontsize=15,
    padding=3,
)
extension_defaults = widget_defaults.copy()


# returns only the application name aka the final word after - or —
def parseWmName(title):
    title2 = re.split("— |-", title)
    return (title2[-1]).strip()

def widgetsList():
    widgets_list =  [
                widget.CurrentLayout(),
                widget.GroupBox(),
                widget.WindowName(parse_text=parseWmName),
                widget.GenPollText(update_interval=1, func=lambda: subprocess.check_output("sh /home/ame/.config/scripts/bar.sh", shell=True, text=True).strip()),
                widget.Clock(format="%a %m/%d %I:%M:%S %p"),
                widget.Systray(),
            ]
    return widgets_list

def s1widget():
    widget = widgetsList()
    return widget

def s2widget():
    widget = widgetsList()
    del widget[5:6]
    return widget


screens = [Screen(top=bar.Bar(widgets=s1widget(), size=20)),
           Screen(top=bar.Bar(widgets=s2widget(), size=20))]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(title="SpeedCrunch"),
        Match(title="Friends List"),
        Match(wm_class="pavucontrol"),
    ],
    border_focus="#3bae4b",
    border_width=4,

)


    



auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
