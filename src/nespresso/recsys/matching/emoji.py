import secrets

import emoji

_COMPLEX_EMOJIES = [
    "\u200d",  # Zero-width joiner
    "\ufe0f",  # Variation selector for emoji style
    "\u0020",  # Space character
    "\u2640",  # Female sign
    "\u2642",  # Male sign
    "\U0001f3fb",
    "\U0001f3fc",
    "\U0001f3fd",
    "\U0001f3fe",
    "\U0001f3ff",  # Skin tone modifiers
    "\u200b",  # Zero-width space
    "\u200c",  # Zero-width non-joiner
    "\u200e",  # Left-to-right mark
    "\u200f",  # Right-to-left mark
    "\u2028",  # Line separator
    "\u2029",  # Paragraph separator
]


def DistinctEmojiList() -> list[str]:
    def IsSimpleEmoji(emj: str) -> bool:
        if "\\U000" in repr(emj):
            return False

        for char in _COMPLEX_EMOJIES:
            if char in emj:
                return False

        return len(emj) == len(emj.encode("utf-16", "surrogatepass").decode("utf-16"))

    def IsNotLetterEmoji(emj: str) -> bool:
        regional_indicator_range = range(0x1F1E6, 0x1F1FF + 1)

        return not all(ord(char) in regional_indicator_range for char in emj)

    emojis = []
    for emj in set(emoji.unicode_codes.EMOJI_DATA.keys()):
        if IsSimpleEmoji(emj) and IsNotLetterEmoji(emj):
            emojis.append(emj)

    emojis = [i for i in emojis if IsSimpleEmoji(i) and IsNotLetterEmoji(i)]

    return emojis


_EMOJIES = DistinctEmojiList()


def RandomEmoji() -> str:
    return secrets.choice(_EMOJIES)
