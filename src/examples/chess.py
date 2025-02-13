from main import TerminalUI
import time


def main():
    with TerminalUI() as tui:
        # Colors for pieces and board
        WHITE_PIECE_COLOR = "#FFFFFF"  # White pieces
        BLACK_PIECE_COLOR = "#2a2a2a"  # Black pieces
        WHITE_SQUARE = "#84888b"
        BLACK_SQUARE = "#546169"

        # Initialize empty board
        chess_board = [[None for _ in range(8)] for _ in range(8)]
        colors = [
            [WHITE_SQUARE if (row + col) % 2 == 0 else BLACK_SQUARE for col in range(8)]
            for row in range(8)
        ]

        # Setup initial pieces with their colors
        white_pieces = {
            (7, 0): "♜",
            (7, 1): "♞",
            (7, 2): "♝",
            (7, 3): "♛",
            (7, 4): "♚",
            (7, 5): "♝",
            (7, 6): "♞",
            (7, 7): "♜",
            (6, 0): "♙",
            (6, 1): "♙",
            (6, 2): "♙",
            (6, 3): "♙",
            (6, 4): "♙",
            (6, 5): "♙",
            (6, 6): "♙",
            (6, 7): "♙",
        }

        black_pieces = {
            (0, 0): "♜",
            (0, 1): "♞",
            (0, 2): "♝",
            (0, 3): "♛",
            (0, 4): "♚",
            (0, 5): "♝",
            (0, 6): "♞",
            (0, 7): "♜",
            (1, 0): "♙",
            (1, 1): "♙",
            (1, 2): "♙",
            (1, 3): "♙",
            (1, 4): "♙",
            (1, 5): "♙",
            (1, 6): "♙",
            (1, 7): "♙",
        }

        # Draw the board base
        board_x, board_y = 8, 3  # Adjusted position to leave room for coordinates
        tui.draw.matrix(
            board_x, board_y, chess_board, cell_width=4, cell_height=3, colors=colors
        )

        # Place pieces on the board
        for pos, piece in white_pieces.items():
            row, col = pos
            chess_board[row][col] = piece

        for pos, piece in black_pieces.items():
            row, col = pos
            chess_board[row][col] = piece

        # Overlay pieces
        for row in range(8):
            for col in range(8):
                x = board_x + 1 + (col * 4)  # Center horizontally in cell
                y = board_y + 1 + (row * 3)  # Center vertically in cell

                if chess_board[row][col]:
                    bg_color = colors[row][col]
                    piece = chess_board[row][col]
                    fg_color = WHITE_PIECE_COLOR if row >= 6 else BLACK_PIECE_COLOR
                    tui.primitives.draw_char(x, y, piece, fg=fg_color, bg=bg_color)

        # Draw title
        tui.draw.string(board_x, 1, "Chess Board", width=32, align="center")

        # Add coordinates with proper spacing
        for i in range(8):
            # Draw file letters (a-h)
            tui.draw.string(board_x + 2 + (i * 4), board_y - 1, chr(97 + i))
            # Draw rank numbers (1-8) from bottom to top
            tui.draw.string(board_x - 2, board_y + 1 + (i * 3), str(8 - i))

        while True:
            tui.render()
            time.sleep(0.1)


if __name__ == "__main__":
    main()
