#!/usr/bin/python
#
#       Curses example program
#
import string

def message(window, text,row=23):
    window.move(row,0)
    window.clrtoeol()
    window.addstr(row,5,text)
    window.refresh()

def sure(win,msg_text):
    while 1:
        message(win,msg_text)
        comm_ch = win.getch()
        ans = chr(comm_ch)
        if ans == 'y':
            return 1
        elif ans == 'n':
            return 0

def ui(win,title="Test"):
    times = 0
    app_string = "Application Title Here"
    if len(app_string) < 79:
        cent = (80-len(title))/2+.5
    else:
        cent = 0
        app_string = app_string[:79]
    win.addstr(0,cent,app_string,curses.A_STANDOUT)
    win.addstr(2,0,string.center(title,79),curses.A_BOLD)
    win.addstr(7,4,"Main window text")

    while 1:
        win.refresh()
        times = times + 1

        if sure(win,"Do you want to quit? (y/n) "):
            break

        if times % 2:
            hwin = curses.newwin(6,25,5,3)
            hwin.clear()
            hwin.addstr(1,2,"Some text in the first box")
            hwin.box()
            hwin.refresh()
        else:
            hwin.clear()
            hwin.touchwin()
            hwin.refresh()

        if times % 3:
            vwin = curses.newwin(16,25,5,30)
            vwin.clear()
            vwin.addstr(1,2,"Some text in the\n second box")
            vwin.box()
            vwin.refresh()
        else:
            vwin.clear()
            vwin.touchwin()
            vwin.refresh()

    hwin.clear()
    hwin.touchwin()
    hwin.refresh()
    vwin.clear()
    vwin.touchwin()
    vwin.refresh()

    win.clear()
    win.refresh()

if __name__=='__main__':
    import curses, traceback
    try:        # Initialize curses
        stdscr=curses.initscr()
        curses.noecho() ; curses.cbreak()
        stdscr.keypad(1)
        ui(stdscr,title="Curses Example Program")         # Enter the main loop
        stdscr.keypad(0)
        curses.echo() ; curses.nocbreak()
        curses.endwin()                 # Terminate curses
    except:
        stdscr.keypad(0)
        curses.echo() ; curses.nocbreak()
        curses.endwin()
        traceback.print_exc()           # Print the exception
