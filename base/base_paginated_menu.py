import discord


class BasePaginatedMenu(discord.ui.View):
    """
    This is a simple paginated menu.

    It is easily customizable by overriding the following methods:

    - get_embed()
    - get_content()
    - get_page_display_value()

    You may also override the following variables:

    - _min_page
    - _max_page
    - _min_jump
    - _max_jump

    Alternatively, you may override their property getters:

    - min_page
    - max_page
    - min_jump
    - max_jump
    """

    def __init__(self):
        super().__init__()
        self.current_page = 0

        self._min_page = 0
        self._max_page = 100

        self.message = None

    @property
    def min_page(self) -> int:
        return self._min_page

    @property
    def max_page(self) -> int:
        return self._max_page

    @property
    def min_jump(self) -> int:
        return self.min_page

    @property
    def max_jump(self) -> int:
        return self.max_page

    async def get_page_display_value(self) -> str:
        """
        This returns the value to display on the display button.
        """
        return str(self.current_page)

    @discord.ui.button(label="<<", style=discord.ButtonStyle.primary)
    async def previous_page_jump(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        This is the previous page jump button.

        It jumps to the first page.
        """
        self.current_page = self.min_page

        await self.refresh(interaction)

    @discord.ui.button(label="<", style=discord.ButtonStyle.primary)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        This is the previous page button.
        """
        self.current_page -= 1
        if self.current_page < self.min_page:
            self.current_page = self.min_jump

        await self.refresh(interaction)

    @discord.ui.button(label="0", style=discord.ButtonStyle.grey)
    async def page_counter(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        This is the page counter button.

        It displays the current page. Pressing it will open a modal to change the page.
        """
        await interaction.response.send_modal(PageSelectModal(self))

    @discord.ui.button(label=">", style=discord.ButtonStyle.primary)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        This is the next page button.
        """
        self.current_page += 1
        if self.current_page > self.max_page:
            self.current_page = self.max_jump

        await self.refresh(interaction)

    @discord.ui.button(label=">>", style=discord.ButtonStyle.primary)
    async def next_page_jump(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        This is the next page jump button.

        It jumps to the last page.
        """
        self.current_page = self.max_page

        await self.refresh(interaction)

    async def optional_button_1_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        This is the optional button 1 callback.

        It is called when the optional button 1 is pressed.
        """
        pass

    @discord.ui.button(label="🔒", style=discord.ButtonStyle.grey, disabled=True)
    async def optional_button_1(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        This is the optional button 1.

        It is disabled by default.
        """
        await self.optional_button_1_callback(interaction, button)

    async def optional_button_2_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        This is the optional button 2 callback.

        It is called when the optional button 2 is pressed.
        """
        pass

    @discord.ui.button(label="🔒", style=discord.ButtonStyle.grey, disabled=True)
    async def optional_button_2(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        This is the optional button 2.

        It is disabled by default.
        """
        await self.optional_button_2_callback(interaction, button)

    @discord.ui.button(label="close", style=discord.ButtonStyle.danger)
    async def close_view(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        This is the close button.

        It closes the menu.
        """
        self.stop()
        # Remove all buttons
        for child in self.children:
            child.disabled = True
        await self.refresh(interaction)

    async def optional_button_3_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        This is the optional button 3 callback.

        It is called when the optional button 3 is pressed.
        """
        pass

    @discord.ui.button(label="🔒", style=discord.ButtonStyle.grey, disabled=True)
    async def optional_button_3(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        This is the optional button 3.

        It is disabled by default.
        """
        await self.optional_button_3_callback(interaction, button)

    async def optional_button_4_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        This is the optional button 4 callback.

        It is called when the optional button 4 is pressed.
        """
        pass

    @discord.ui.button(label="🔒", style=discord.ButtonStyle.grey, disabled=True)
    async def optional_button_4(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        This is the optional button 4.

        It is disabled by default.
        """
        await self.optional_button_4_callback(interaction, button)

    async def start(self, interaction: discord.Interaction, *args, **kwargs):
        """
        This is the start method for the menu.

        It is called to start & send the menu.

        By default, it uses the `get_embed` and `get_content` methods to create the embed and content.
        This can be overridden by passing in a `embed` and `content` keyword argument.
        """
        if interaction.is_expired():
            return

        content = await self.get_content()
        embed = await self.get_embed()

        embed = await self.post_embed(embed)

        kwargs.setdefault('content', content)
        kwargs.setdefault('embed', embed)

        await self.refresh_page_display_button()
        if interaction.response.is_done():
            self.message = await interaction.followup.send(*args, **kwargs, view=self)
            return
        self.message = await interaction.response.send_message(*args, **kwargs, view=self)

    async def refresh_page_display_button(self):
        """
        This is the refresh method for the display button.

        It refreshes the display button, using the `get_display_value` method.
        """
        self.children[2].label = await self.get_page_display_value()

    async def refresh(self, interaction: discord.Interaction):
        """
        This is the refresh method for the menu.

        It refreshes the embed, content and view, using the `get_embed` and `get_content` methods.
        """
        content = await self.get_content()
        embed = await self.get_embed()

        embed = await self.post_embed(embed)

        await self.refresh_page_display_button()
        await interaction.response.edit_message(content=content, embed=embed, view=self)

    async def get_embed(self) -> discord.Embed:
        """
        This is the embed method for the menu.

        It is called to create the embed.
        :return: The embed to send.
        """
        embed = discord.Embed(title='Page {}'.format(self.current_page))
        embed.description = 'This is page {}'.format(self.current_page)
        return embed

    async def post_embed(self, embed: discord.Embed) -> discord.Embed:
        """
        This is the post embed method for the menu.

        It is called after the get_embed method, but before the embed is sent.
        :param embed: The embed to send.
        :return: The embed to send.
        """
        if embed.footer.text is None and embed.footer.icon_url is None:
            embed.set_footer(text=f"Page {self.current_page + 1}/{self.max_page + 1}")

        return embed

    async def get_content(self) -> str:
        """
        This is the content method for the menu.

        It is called to create the (message) content.
        :return: The content to send.
        """
        return ""

    async def jump_to_page(self, page: int, interaction: discord.Interaction):
        """
        This is the jump to page method for the menu.

        It is called to jump to a specific page.
        :param page: The page to jump to.
        :param interaction: The interaction that triggered the jump.
        """
        # Clamp the page to the min and max page.
        page = max(self.min_page, min(self.max_page, page))

        self.current_page = page
        await self.refresh(interaction)


class PageSelectModal(discord.ui.Modal, title="Select a page"):
    """
    Very simple modal for selecting a page.
    """

    def __init__(self, menu: BasePaginatedMenu, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.menu = menu

    page_jump = discord.ui.TextInput(label='Page to jump to', placeholder='0', min_length=1, max_length=4)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        """
        This is the on submit method for the modal.

        It is called when the modal is submitted.
        """
        try:
            page = int(self.page_jump.value) - 1
        except ValueError:
            return

        await self.menu.jump_to_page(page, interaction)
        self.stop()

    async def on_timeout(self) -> None:
        """
        This is the on timeout method for the modal.

        It is called when the modal times out.
        """
        self.stop()
