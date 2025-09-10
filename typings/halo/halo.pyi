"""
This file is a stub for the Halo package, providing type hints for its public API.
"""

from typing import IO

class Halo:
    """Halo library.
    Attributes
    ----------
    CLEAR_LINE : str
        Code to clear the line
    """

    CLEAR_LINE: str = ...
    SPINNER_PLACEMENTS: list[str] = ...
    def __init__(
        self,
        text: str | None = ...,
        color: str | None = ...,
        text_color: str | None = ...,
        spinner: str | dict | None = ...,
        animation: str | None = ...,
        placement: str | None = ...,
        interval: int | None = ...,
        enabled: bool | None = ...,
        stream: IO | None = ...,
    ) -> None:
        """Constructs the Halo object.
        Parameters
        ----------
        text : str, optional
            Text to display.
        text_color : str, optional
            Color of the text.
        color : str, optional
            Color of the text to display.
        spinner : str|dict, optional
            String or dictionary representing spinner. String can be one of 60+ spinners
            supported.
        animation: str, optional
            Animation to apply if text is too large. Can be one of `bounce`, `marquee`.
            Defaults to ellipses.
        placement: str, optional
            Side of the text to place the spinner on. Can be `left` or `right`.
            Defaults to `left`.
        interval : integer, optional
            Interval between each frame of the spinner in milliseconds.
        enabled : boolean, optional
            Spinner enabled or not.
        stream : io, optional
            Output.
        """

    def __enter__(self):  # -> Self:
        """Starts the spinner on a separate thread. For use in context managers.
        Returns
        -------
        self
        """

    def __exit__(self, type, value, traceback):  # -> None:
        """Stops the spinner. For use in context managers."""

    def __call__(self, f):  # -> _Wrapped[Callable[..., Any], Any, Callable[..., Any], Any]:
        """Allow the Halo object to be used as a regular function decorator."""

    @property
    def spinner(self):  # -> dict[Any, Any] | dict[str, int | list[str]]:
        """Getter for spinner property.
        Returns
        -------
        dict
            spinner value
        """

    @spinner.setter
    def spinner(self, spinner: dict | str):  # -> None:
        """Setter for spinner property.
        Parameters
        ----------
        spinner : dict, str
            Defines the spinner value with frame and interval
        """

    @property
    def text(self):  # -> list[Any]:
        """Getter for text property.
        Returns
        -------
        str
            text value
        """

    @text.setter
    def text(self, text: str):  # -> None:
        """Setter for text property.
        Parameters
        ----------
        text : str
            Defines the text value for spinner
        """

    @property
    def text_color(self):  # -> None:
        """Getter for text color property.
        Returns
        -------
        str
            text color value
        """

    @text_color.setter
    def text_color(self, text_color: str):  # -> None:
        """Setter for text color property.
        Parameters
        ----------
        text_color : str
            Defines the text color value for spinner
        """

    @property
    def color(self):  # -> str:
        """Getter for color property.
        Returns
        -------
        str
            color value
        """

    @color.setter
    def color(self, color: str):  # -> None:
        """Setter for color property.
        Parameters
        ----------
        color : str
            Defines the color value for spinner
        """

    @property
    def placement(self):  # -> str:
        """Getter for placement property.
        Returns
        -------
        str
            spinner placement
        """

    @placement.setter
    def placement(self, placement: str):  # -> None:
        """Setter for placement property.
        Parameters
        ----------
        placement: str
            Defines the placement of the spinner
        """

    @property
    def spinner_id(self):  # -> str | None:
        """Getter for spinner id
        Returns
        -------
        str
            Spinner id value
        """

    @property
    def animation(self):  # -> None:
        """Getter for animation property.
        Returns
        -------
        str
            Spinner animation
        """

    @animation.setter
    def animation(self, animation: str):  # -> None:
        """Setter for animation property.
        Parameters
        ----------
        animation: str
            Defines the animation of the spinner
        """

    def clear(self) -> None:
        """Clears the line and returns cursor to the start.
        of line
        Returns
        -------
        self
        """

    def render(self):  # -> Self:
        """Runs the render until thread flag is set.
        Returns
        -------
        self
        """

    def frame(self):  # -> str:
        """Builds and returns the frame to be rendered
        Returns
        -------
        self
        """

    def text_frame(self):  # -> str:
        """Builds and returns the text frame to be rendered
        Returns
        -------
        self
        """

    def start(self, text: str | None = None) -> None:
        """Starts the spinner on a separate thread.
        Parameters
        ----------
        text : None, optional
            Text to be used alongside spinner
        Returns
        -------
        self
        """

    def stop(self):  # -> Self:
        """Stops the spinner and clears the line.
        Returns
        -------
        self
        """

    def succeed(self, text: str | None = None) -> None:
        """Shows and persists success symbol and text and exits.
        Parameters
        ----------
        text : None, optional
            Text to be shown alongside success symbol.
        Returns
        -------
        self
        """

    def fail(self, text: str | None = None) -> None:
        """Shows and persists fail symbol and text and exits.
        Parameters
        ----------
        text : None, optional
            Text to be shown alongside fail symbol.
        Returns
        -------
        self
        """

    def warn(self, text=...):  # -> Self:
        """Shows and persists warn symbol and text and exits.
        Parameters
        ----------
        text : None, optional
            Text to be shown alongside warn symbol.
        Returns
        -------
        self
        """

    def info(self, text: str | None = None):  # -> Self:
        """Shows and persists info symbol and text and exits.
        Parameters
        ----------
        text : None, optional
            Text to be shown alongside info symbol.
        Returns
        -------
        self
        """

    def stop_and_persist(self, symbol: str | None = None, text: str | None = None) -> None:
        """Stops the spinner and persists the final frame to be shown.
        Parameters
        ----------
        symbol : str, optional
            Symbol to be shown in final frame
        text: str, optional
            Text to be shown in final frame

        Returns
        -------
        self
        """
