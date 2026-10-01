"""windytranslate find en sw [--all] [--notice] | windytranslate translate en fr "text" """
import argparse
import sys

from .catalogue import candidates


def _describe(m) -> str:
    q = (f"chrF++ {m.chrf} ({m.score.get('band')}) on {m.score.get('benchmark', 'FLORES-200')}"
         if m.chrf is not None else "not yet scored")
    flag = "" if m.licence_clear else f"  [licence note: {m.licence_status}]"
    return f"{m.repo}\n  {m.name}\n  quality: {q}\n  licence: {m.licence}{flag}\n  page:    {m.page}"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="windytranslate", description="Windstorm Labs open models (windytranslate.com)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("find", help="best model for a language pair")
    f.add_argument("src"); f.add_argument("tgt")
    f.add_argument("--all", action="store_true"); f.add_argument("--notice", action="store_true")
    t = sub.add_parser("translate", help='translate locally (pip install "windytranslate[local]")')
    t.add_argument("src"); t.add_argument("tgt"); t.add_argument("text", nargs="+")
    a = ap.parse_args(argv)
    if a.cmd == "find":
        found = candidates(a.src, a.tgt)
        if not found:
            print(f"No model for {a.src} -> {a.tgt}. Browse https://windytranslate.com/languages", file=sys.stderr)
            return 1
        for m in (found if a.all else found[:1]):
            print(_describe(m))
            if a.notice:
                print("\n--- NOTICE (ship this with your product) ---\n" + m.notice)
            print()
        return 0
    from .local import translate
    print(translate(" ".join(a.text), a.src, a.tgt))
    return 0


if __name__ == "__main__":
    sys.exit(main())
