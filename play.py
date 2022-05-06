from minesweeper import Game, Size

game = Game(Size(5, 5), 5, False)
game.board.print()
keep_playing = 'play'
while keep_playing == 'play':
    try:
        print('move?')
        move = input()
        print('X?')
        x = int(input())
        print('Y?')
        y = int(input())
        result = game.play_round(x, y, move)
        keep_playing = result[0]
    except Exception as e:
        print(e)
        continue
game.board.debug = True
game.board.print()
