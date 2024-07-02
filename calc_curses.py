import curses

Btn_List = []
Btn_W = 5
Btn_H = 1
Btn_Pos_X = 1
Btn_Pos_Y = 3
Btn_Gap_X = 1
Btn_Gap_Y = 1

Disp_Text = ""
Disp_X = 1
Disp_Y = 1
Disp_W = 29


def init_button(btn_rows):
  for row, btn_row in enumerate(btn_rows):
    for col, (label, pair_num) in enumerate(btn_row):
      bx = Btn_Pos_X + (col * (Btn_W + Btn_Gap_X))
      by = Btn_Pos_Y + (row * (Btn_H + Btn_Gap_Y))
      Btn_List.append([label, bx, by, pair_num])


def main(stdscr):
  global Disp_Text

  stdscr.clear()

  curses.curs_set(0)
  curses.mousemask(curses.ALL_MOUSE_EVENTS)
  curses.start_color()
  curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
  curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)
  curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)
  curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)

  init_button([
      # Label, Color Pair Number
      [[" ", 3], [" ", 3], [" ", 3], ["C", 3], ["B", 3]],
      [["7", 1], ["8", 1], ["9", 1], ["/", 2], ["(", 2]],
      [["4", 1], ["5", 1], ["6", 1], ["*", 2], [")", 2]],
      [["1", 1], ["2", 1], ["3", 1], ["+", 2], [" ", 2]],
      [[" ", 1], ["0", 1], [".", 1], ["-", 2], ["=", 2]]
  ])

  # Menampilkan Tombol
  for label, bx, by, pair_number in Btn_List:
    stdscr.addstr(by, bx, f"{label:^{Btn_W}}", curses.color_pair(pair_number))

  stdscr.refresh()

  calc_err = False

  while True:
    # Menampilkan Displat Teks
    stdscr.addstr(Disp_Y, Disp_X, f"{Disp_Text:<{Disp_W}}",
                  curses.color_pair(4))
    stdscr.refresh()

    key = stdscr.getch()

    if key == ord("q"):
      break

    if key == curses.KEY_MOUSE:
      try:
        # id, mx, my, mz, bsate
        _, mx, my, _, _ = curses.getmouse()

        for label, bx, by, _ in Btn_List:
          if (bx + Btn_W) > mx >= bx and my == by:
            if label == " ":
              break

            if calc_err:
              calc_err = False
              Disp_Text = ""

            if label == "C":
              Disp_Text = ""
            elif label == "B":
              Disp_Text = Disp_Text[:-1]
            elif label == "=":
              Disp_Text = str(eval(Disp_Text))

              # 50 / 5 = 5.0
              if "." in Disp_Text:
                Disp_Text = Disp_Text.rstrip("0").rstrip(".")
            else:
              Disp_Text += label

            break
      except Exception:
        calc_err = True
        Disp_Text = "Error"


if __name__ == "__main__":
  curses.wrapper(main)
