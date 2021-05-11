
from markdown.inlinepatterns import InlineProcessor
from markdown.extensions import Extension

GREEK = {
    "alpha" : "&alpha;",
    "Alpha" : "&Alpha;",
    "beta" : "&beta;",
    "Beta" : "&Beta;",
    "gamma" : "&gamma;",
    "Gamma" : "&Gamma;",
    "delta" : "&delta;",
    "Delta" : "&Delta;",
    "epsilon" : "&epsilon;",
    "Epsilon" : "&Epsilon;",
    "zeta" : "&zeta;",
    "Zeta" : "&Zeta;",
    "eta" : "&eta;",
    "Eta" : "&Eta;",
    "theta" : "&theta;",
    "Theta" : "&Theta;",
    "iota" : "&iota;",
    "Iota" : "&Iota;",
    "kappa" : "&kappa;",
    "Kappa" : "&Kappa;",
    "lambda" : "&lambda;",
    "Lambda" : "&Lambda;",
    "mu" : "&mu;",
    "Mu" : "&Mu;",
    "nu" : "&nu;",
    "Nu" : "&Nu;",
    "xi" : "&xi;",
    "Xi" : "&Xi;",
    "omicron" : "&omicron;",
    "Omicron" : "&Omicron;",
    "pi" : "&pi;",
    "Pi" : "&Pi;",
    "rho" : "&rho;",
    "Rho" : "&Rho;",
    "sigma" : "&sigma;",
    "Simga" : "&Simga;",
    "sigmaf" : "&sigmaf;",
    "tau" : "&tau;",
    "Tau" : "&Tau;",
    "upsilon" : "&upsilon;",
    "Upsilon" : "&Upsilon;",
    "phi" : "&phi;",
    "Phi" : "&Phi;",
    "chi" : "&chi;",
    "Chi" : "&Chi;",
    "psi" : "&psi;",
    "Psi" : "&Psi;",
    "omega" : "&omega;",
    "Omega" : "&Omega;",
}
# Add accent characters
GREEK.update({
    "omicronacute" : "&oacute;",
    "Omicronacute" : "&Oacute;"
})


HEBREW = {
    "alef" : "&#x05D0;",
    "bet" : "&#x05D1;",
    "gimel" : "&#x05D2;",
    "dalet" : "&#x05D3;",
    "he" : "&#x05D4;",
    "vav" : "&#x05D5;",
    "zayin" : "&#x05D6;",
    "het" : "&#x05D7;",
    "tet" : "&#x05D8;",
    "yod" : "&#x05D9;",
    "kaff" : "&#x05DA;",
    "kaf" : "&#x05DB;",
    "lamed" : "&#x05DC;",
    "memf" : "&#x05DD;",
    "mem" : "&#x05DE;",
    "nunf" : "&#x05DF;",
    "nun" : "&#x05E0;",
    "samekh" : "&#x05E1;",
    "ayin" : "&#x05E2;",
    "pef" : "&#x05E3;",
    "pe" : "&#x05E4;",
    "tsadif" : "&#x05E5;",
    "tsadi" : "&#x05E6;",
    "qof" : "&#x05E7;",
    "resh" : "&#x05E8;",
    "shin" : "&#x05E9;",
    "tav" : "&#x05EA;"
}

class ReplaceLeaderInline(InlineProcessor):
    """Replaces characters of type `\string` from a dictionary"""
    def __init__(self, replace_map, *args, **kwargs):
        super().__init__(r"\\([^\b\\&]+)", *args, **kwargs)
        self.map = replace_map

    def handleMatch(self, m, data):
        el, start, end = None, None, None
        try:
            el = self.map[m.group(1)]
        except KeyError:
            pass
            # print(m.groups())
        else:
            start = m.start(0)
            end = m.end(0)

        return el, start, end

class BibicalLanguageExtension(Extension):
    def extendMarkdown(self, md):
        md.inlinePatterns.register(
            ReplaceLeaderInline(GREEK,md),
            'greek_replace',
            1000
        )
        md.inlinePatterns.register(
            ReplaceLeaderInline(HEBREW,md),
            'hebrew_replace',
            1001
        )
