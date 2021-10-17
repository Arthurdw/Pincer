# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING
from dataclasses import dataclass

from ...utils.types import MISSING
from ...utils.api_object import APIObject

if TYPE_CHECKING:
    from typing import Optional

    from ...client import Client
    from ...utils.types import APINullable
    from ...utils.snowflake import Snowflake
    from ...utils.conversion import convert, construct_client_dict


class PremiumTypes(IntEnum):
    """The type of Discord premium a user has.

    Attributes
    ----------
    NONE:
    NITRO_CLASSIC:
    NITRO:
    """  # TODO: docs: again
    NONE = 0
    NITRO_CLASSIC = 1
    NITRO = 2


class VisibilityType(IntEnum):
    """The type of a connection visibility.

    Attributes
    ----------
    NONE:
    EVERYONE:
    """  # TODO docs: once more
    NONE = 0
    EVERYONE = 1


@dataclass
class User(APIObject):
    """Represents a Discord user. This can be a bot account or a
    human account.

    Attributes
    ----------
    avatar: Optional[:class:`str`]
        The user's avatar hash
    discriminator: :class:`str`
        The user's 4-digit discord-tag
    id: :class:`~pincer.utils.snowflake.Snowflake`
        The user's id
    username: :class:`str`
        The user's username, not unique across the platform
    flags: APINullable[:class:`int`]
        The flags on a user's account
    accent_color: APINullable[Optional[:class:`int`]]
        The user's banner color encoded as an integer representation of
        hexadecimal color code
    banner: APINullable[Optional[:class:`str`]]
        The user's banner, or null if unset
    banner_color: APINullable[Optional[:class:`int`]]
        The color of the user's banner
    bot: APINullable[:class:`bool`]
        Whether the user belongs to an OAuth2 application
    email: APINullable[Optional[:class:`str`]]
        The user's email
    locale: APINullable[:class:`str`]
        The user's chosen language option
    mfa_enabled: APINullable[:class:`bool`]
        Whether the user has two factor enabled on their account
    premium_type: APINullable[:class:`int`]
        The type of Nitro subscription on a user's account
    public_flags: APINullable[:class:`int`]
        The public flags on a user's account
    system: APINullable[:class:`bool`]
        Whether the user is an Official Discord System user
        (part of the urgent message system)
    verified: APINullable[:class:`bool`]
        Whether the email on this account has been verified
    """
    avatar: Optional[str]
    discriminator: str
    id: Snowflake
    username: str

    flags: APINullable[int] = MISSING
    accent_color: APINullable[Optional[int]] = MISSING
    banner: APINullable[Optional[str]] = MISSING
    banner_color: APINullable[Optional[int]] = MISSING
    bot: APINullable[bool] = MISSING
    email: APINullable[Optional[str]] = MISSING
    locale: APINullable[str] = MISSING
    mfa_enabled: APINullable[bool] = MISSING
    premium_type: APINullable[int] = MISSING
    public_flags: APINullable[int] = MISSING
    system: APINullable[bool] = MISSING
    verified: APINullable[bool] = MISSING

    @property
    def premium(self) -> APINullable[PremiumTypes]:
        """APINullable[:class:`~pincer.objects.user.user.PremiumTypes`]: The
        user their premium type in a usable enum.
        """
        return (
            MISSING
            if self.premium_type is MISSING
            else PremiumTypes(self.premium_type)
        )

    @property
    def mention(self) -> str:
        """:class:`str`: The user's mention string.
        """
        return f"<@!{self.id}>"

    def __str__(self):
        return self.username + '#' + self.discriminator

    def __post_init__(self):
        self.id = convert(self.id, Snowflake.from_string)

    @classmethod
    async def from_id(cls, client: Client, user_id: int) -> User:
        data = await client.http.get(f"users/{user_id}")
        return cls.from_dict(construct_client_dict(client, data))
