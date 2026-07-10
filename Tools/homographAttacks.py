import argparse
import itertools

HOMOGLYPH_POOL = {
    'a': ['a', 'а', 'ɑ', 'ǎ', 'ā'],
    'b': ['b', 'Ь', 'ｂ'],
    'c': ['c', 'с', 'ｃ'],
    'd': ['d', 'ԁ', 'ｄ'],
    'e': ['e', 'е', 'ｅ', 'ė', 'ē'],
    'f': ['f', 'ｆ'],
    'g': ['g', 'ɡ', 'ｇ'],
    'h': ['h', 'һ', 'ｈ'],
    'i': ['i', 'і', 'í', 'ɩ', 'ꮎ', '𝑖', 'Ӏ'],
    'j': ['j', 'ј', 'ｊ'],
    'k': ['k', 'к', 'ｋ'],
    'l': ['l', 'ⅼ', 'ｌ'],
    'm': ['m', 'ｍ'],
    'n': ['n', 'ո', 'ｎ', 'ᐪ', 'ŋ'],
    'o': ['o', 'о', 'ο', 'ｏ'],
    'p': ['p', 'р', 'ｐ'],
    'q': ['q', 'ｑ'],
    'r': ['r', 'ｒ'],
    's': ['s', 'ѕ', 'ｓ'],
    't': ['t', 'ｔ'],
    'u': ['u', 'υ', 'ｕ'],
    'v': ['v', 'ν', 'ｖ'],
    'w': ['w', 'ԝ', 'ｗ'],
    'x': ['x', 'х', 'ｘ'],
    'y': ['y', 'у', 'ｙ'],
    'z': ['z', 'ｚ'],
    '1': ['1', '１'],
}

def generate_homographs(target_word):
    choices = [HOMOGLYPH_POOL.get(char.lower(), [char]) for char in target_word]

    all_combos = itertools.product(*choices)

    print(f"[*] Target string: {target_word}")
    print(f"{'UNICODE VARIANT':<20} | {'PUNYCODE (IDNA)'}")
    print("-" * 50)

    valid_count = 0
    for combo in all_combos:
        variant = "".join(combo)

        if variant.lower() != target_word.lower():
            try:
                punycode = variant.encode('idna').decode('utf-8')

                if punycode == target_word.lower():
                    continue

                print(f"{variant:<20} | {punycode}")
                valid_count += 1
            except (UnicodeEncodeError, ValueError):
                continue

    print("-" * 50)
    print(f"[*] Generated {valid_count} functional variations.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate robust homoglyph combinations.")
    parser.add_argument("-u", "--username", required=True, help="The target string to spoof")

    args = parser.parse_args()
    generate_homographs(args.username)
