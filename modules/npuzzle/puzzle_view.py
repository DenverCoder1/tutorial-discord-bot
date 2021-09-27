from typing import List

import nextcord

from .board_state import BoardState


class NPuzzleButton(nextcord.ui.Button['NPuzzleView']):
    def __init__(self, col: int, row: int, num: int):
        label = num if num > 0 else '\u200b'
        disabled = num == 0
        super().__init__(style=nextcord.ButtonStyle.secondary,
                         label=label, disabled=disabled, row=row)
        self.col = col
        self.row = row

    async def callback(self, interaction: nextcord.Interaction):
        assert self.view is not None
        view: NPuzzleView = self.view
        state = view.state
        size = state.size
        content = interaction.message.content

        state.swap_tile_with_empty(self.row * size + self.col)

        for child in view.children:
            num = state.board[child.row * size + child.col]
            child.label = num if num > 0 else '\u200b'
            child.disabled = num == 0

        if state.is_target():
            content = f"Congratulations! You won in {state.path_length()} moves! :tada:"
            for child in view.children:
                child.disabled = True
            view.stop()

        await interaction.response.edit_message(content=content, view=view)


class NPuzzleView(nextcord.ui.View):
    children: List[NPuzzleButton]

    def __init__(self, size: int):
        super().__init__()
        self.size = size
        self.state = BoardState.init_from_random(size)

        for col in range(size):
            for row in range(size):
                self.add_item(
                    NPuzzleButton(
                        col, row, self.state.board[row * size + col])
                )
