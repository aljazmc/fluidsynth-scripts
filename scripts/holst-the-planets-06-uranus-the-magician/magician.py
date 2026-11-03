from orchestra import Orchestra
from piano import run

# Holst, The Planets, VI. Uranus, the Magician. A from-memory arrangement for
# General MIDI orchestra: the four-note spell G, E-flat, A, B (Holst's
# initials, G-S-T-H) thundered by brass, tubas and timpani, the bassoons'
# clumsy dance, the march, the organ's sweep at the climax and the sudden
# vanishing follow Holst, the notes are approximate.
SEED = 1920

PARTS = ("flutes", "clarinets", "bassoons", "horns", "trumpets", "trombones", "tuba", "timpani",
         "harp", "organ", "violins", "violas", "cellos", "basses", "pizzicato", "percussion")

SPELL = "m4/4 g4:2^ eb5:2^ | a4:2^ b4:2^ |"
SPELL_FAST = "m4/4 g3:1^ eb4:1^ a3:1^ b3:1^ |"
SPELL_DRUM = "m4/4 g2:1/2^ eb3:1/2^ a2:1/2^ b2:1/2^ r:2 |"

# Allegro, 6/8 (three crotchet beats a bar)
DANCE = ("m6/8 c3:1/2' g2' c3' e3' d3' c3' | b2' g2' b2' d3:1' r:1/2 | "
         "c3:1/2' g2' c3' e3' f3' g3' | a3:1' g3:1/2' e3:1' r:1/2 |")
DANCE_PLUCK = "m6/8 " + " ".join(["c2:1/2' r:1 g2:1/2' r:1 |"] * 4)
MARCH = ("m6/8 g4:1^ g4:1/2 c5:1^ c5:1/2 | e5:3/2^ d5:3/2 | c5:1 b4:1/2 a4:1 g4:1/2 | g4:3 | "
         "a4:1^ a4:1/2 d5:1^ d5:1/2 | f5:3/2^ e5:3/2 | d5:1 c5:1/2 b4:1 a4:1/2 | g4:3 |")
MARCH_BASS = "m6/8 " + " ".join(["c3:1' g2:1/2' c3:1' g2:1/2' |", "g2:1' d3:1/2' g2:1' d3:1/2' |"] * 4)


def picture(orchestra):
    # the spell: brass, then tubas, then timpani
    orchestra.play({"trumpets": "!fff " + SPELL, "trombones": ("!fff " + SPELL, -12),
                    "horns": ("!ff " + SPELL, -12)}, bpm=60, gap=0.4, label="spell")
    orchestra.play({"tuba": ("!ff " + SPELL_FAST, -12), "trombones": ("!ff " + SPELL_FAST, -12)},
                   bpm=80, gap=0.3)
    orchestra.play({"timpani": "!ff " + SPELL_DRUM}, bpm=100, gap=0.3)
    orchestra.play({"timpani": "!f " + SPELL_DRUM}, bpm=140, gap=0.6)

    # the dance
    orchestra.play({"bassoons": "!mf " + DANCE, "pizzicato": "!mf " + DANCE_PLUCK}, bpm=180, label="dance")
    orchestra.play({"bassoons": "!f " + DANCE, "clarinets": ("!mf " + DANCE, 12),
                    "pizzicato": "!f " + DANCE_PLUCK, "timpani": "!mf " + DANCE_PLUCK},
                   bpm=180)
    orchestra.play({"violins": ("!f " + DANCE, 24), "flutes": ("!f " + DANCE, 24),
                    "violas": ("!f " + DANCE, 12), "bassoons": "!f " + DANCE,
                    "horns": "!f m6/8 " + " ".join(["c4+e4+g4:1/2^ r:5/2 |"] * 4),
                    "pizzicato": "!f " + DANCE_PLUCK, "timpani": "!f " + DANCE_PLUCK}, bpm=180)

    # the march, growing wilder
    for dynamic in ("f", "ff"):
        orchestra.play({"trumpets": f"!{dynamic} " + MARCH, "horns": (f"!{dynamic} " + MARCH, -12),
                        "violins": (f"!{dynamic} " + MARCH, 12), "trombones": f"!{dynamic} " + MARCH_BASS,
                        "tuba": (f"!{dynamic} " + MARCH_BASS, -12), "cellos": f"!{dynamic} " + MARCH_BASS,
                        "basses": (f"!{dynamic} " + MARCH_BASS, -12), "timpani": f"!{dynamic} " + MARCH_BASS,
                        "percussion": f"!{dynamic} m6/8 " + " ".join(["36:1 38:1/2 36:1 38:1/2 |"] * 8)},
                       bpm=168, label="march")

    # the climax: the spell on everything, the organ sweeping down
    orchestra.play({"trumpets": "!fff " + SPELL, "trombones": ("!fff " + SPELL, -12),
                    "horns": ("!fff " + SPELL, -12), "violins": ("!fff " + SPELL, 12),
                    "tuba": ("!fff " + SPELL, -24), "basses": ("!fff " + SPELL, -24),
                    "timpani": "!fff m4/4 g2:2^ eb3:2^ | a2:2^ b2:2^ |",
                    "percussion": "!fff m4/4 49+36:4 | 49+36:4 |"}, bpm=56, label="climax")
    orchestra.play({"organ": "!fff " + run("c7", "c3", step="1/12") + " c2+c3+g3+c4:3"}, bpm=60)

    # sudden quiet: the magician vanishes, almost
    orchestra.rest(0.8)
    orchestra.play({"violins": "!ppp m4/4 " + " ".join(["g5:1/8 a5"] * 16) + " |",
                    "harp": "!pp m4/4 g3:1 eb4:1 a3:1 b3:1 |",
                    "violas": "!ppp m4/4 eb4+a4:4 |"}, bpm=40, gap=0.5, label="vanishing")
    orchestra.play({"trumpets": "!ff m4/4 g4:1^ eb5:1^ a4:1^ b4:1^ |",
                    "trombones": "!ff m4/4 g3:1^ eb4:1^ a3:1^ b3:1^ |"}, bpm=90, gap=0.6)
    orchestra.play({"harp": "!pp m4/4 g3:1 eb4:1 a3:1 b3:1 | g2+eb3+a3+b3:4 |",
                    "violins": "!ppp m4/4 r:4 | g5+b5:4 !>n |", "basses": "!ppp m4/4 r:4 | g1:4 !>n |"},
                   bpm=40, to=32, label="gone")


def magician():
    orchestra = Orchestra(*PARTS, seed=SEED)
    picture(orchestra)
    return orchestra.render(tail=6.0)
