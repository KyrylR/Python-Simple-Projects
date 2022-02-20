from difflib import SequenceMatcher

from ahk import AHK

ahk = AHK()


def get_deepl_app():
    for window in ahk.windows():
        win_str = window.title.title().decode('cp1252')
        if SequenceMatcher(a=win_str, b='DeepL').ratio() > 0.6:
            return window, win_str

    return None, None


if __name__ == "__main__":
    (win, win_name) = get_deepl_app()
    if win_name is not None:
        print(win_name)

    print(win)
