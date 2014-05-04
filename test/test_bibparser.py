# coding:utf-8

import prepare
prepare
from collections import Counter
from sep.lib import regbibparser
from sep.service import biblio

def test_bibitem():
    i0 = u"Lipton, P., 1998. “The Epistemology of Testimony,” <em>Studies in History and</em>, <em>Philosophy of Science</em>, 29: 1–31."
    p0 = regbibparser.parseitem(i0)
    assert 1998 == p0['year']
    assert 'P. Lipton' == p0['author']
    assert 'The Epistemology of Testimony' == p0['title']
    i1 = "<li><em>Ethica seu Scito teipsum</em>. Edited by R. M. Ilgner in <em>Petri Abaelardi opera theologica</em>. Corpus christianorum (continuatio mediaevalis) Vol. 190. Brepols: Turnholt 2001.</li>"
    p1 = regbibparser.parseitem(i1)
    assert p1 is None
    #assert 2001 == p1['year']
    #assert 'Ethica seu Scito teipsum' == p1['title']

    i2 = u"<li>Fairweather, E. R. (1995) <em>A Scholastic Miscellany</em>. Westminster: John Knox Press. Excerpt from Abelard's commentary on <em>Romans</em>.</li>"
    p2 = regbibparser.parseitem(i2)
    assert 1995 == p2['year']
    assert 'E.R. Fairweather' == p2['author']
    assert 'A Scholastic Miscellany' == p2['title']

    i3 = u"Davidson, Donald, 1963. “Actions, Reasons, Causes,” in Davidson 1980: 3–19"
    p3 = regbibparser.parseitem(i3)
    assert 1963 == p3['year']
    assert 'paper' == p3.type()
    assert 'Actions, Reasons, Causes' == p3['title']

    i4 = u'<li>Hitchcock, C., 2008. “Probabilistic causation,” The Stanford Encyclopedia of Philosophy, Edward N. Zalta(ed.), URL = &lt;<a href="http://plato.stanford.edu/archives/fall2008/entries/causation-probabilistic/">http://plato.stanford.edu/archives/fall2008/entries/causation-probabilistic/</a>&gt;.</li>'
    p4 = regbibparser.parseitem(i4)
    assert 2008 == p4['year']
    assert 'Probabilistic causation' == p4['title']

    i5 = u'<li>–––, 1977b, “Is Turn About Fair Play?” in Gross (ed.), 379–408.</li>'
    p5 = regbibparser.parseitem(i5)
    assert 1977 == p5['year']

    i6 = u'<li>Allen, Lydia D., 1998, “Physics, frivolity, and ‘Madame Pompon-Newton’: the historical reception of the Marquise du Châtelet from 1750–1966”, Ph.D. Dissertation,.University of Cincinnati.</li>'
    p6 = regbibparser.parseitem(i6)
    assert p6 is not None

    i7 = u"––– (ed.), 1991: <em>Paris-Vienne au XIV<sup>e</sup> siècle. Itinéraires d'Albert de Saxe</em> (Actes de la table ronde internationale, Paris, 19–22 juin 1990), Paris: Vrin. [21 articles representing the state of research on Albert's logic and natural philosophy]"
    p7 = regbibparser.parseitem(i7)
    assert p7 is not None
    assert p7['year'] == 1991
    assert p7['title'] == "Paris-Vienne au XIV<sup>e</sup> siècle. Itinéraires d'Albert de Saxe"

    i8 = u"<li>Cohen, J. (ed.), 1996, <em>For Love of Country: Debating the Limits of Patriotism</em>, Boston: Beacon Press.</li>"
    p8 = regbibparser.parseitem(i8)
    assert 1996  == p8['year']
    assert 'For Love of Country: Debating the Limits of Patriotism' == p8['title']
    assert 'J. Cohen (ed.)' == p8['author']

    i9 = u"<li>Einstein, A. 1954. “What is the theory of relativity”. In <em>Ideasand Opinions</em>, pages 227–––232. Bonanza Books, New York.</li>"
    p9 = regbibparser.parseitem(i9)
    assert 1954  == p9['year']
    assert 'What is the theory of relativity' == p9['title']
    assert 'A. Einstein' == p9['author']

    i10 = u"<li>Brittain, C., <em>Philo of Larissa</em> (Oxford 2001), 345–70.</li>"
    p10 = regbibparser.parseitem(i10)
    assert 2001  == p10['year']
    assert 'Philo of Larissa' == p10['title']
    assert 'C. Brittain' == p10['author']

    i11 = u"Raz, Joseph (1986), <em>The Morality of Freedom</em>, Oxford: Oxford University Press."
    p11 = regbibparser.parseitem(i11)
    assert 1986  == p11['year']
    assert 'The Morality of Freedom' == p11['title']
    assert 'Joseph Raz' == p11['author']

    i12 = u"Quine, W. V. O., 1953, “Two Dogmas of Empiricism,” From a Logical Point of View, Cambridge, MA: Harvard University Press. First version of the paper, without any reference to Duhem, in The<em> Philosophical Review</em>, 60 (1951): 20–53."
    p12 = regbibparser.parseitem(i12)
    assert 'W.V.O. Quine' == p12['author']

    i13 = u"Lewis, David, and Gideon Rosen, 2003, “Postscript to ‘Things Qua Truth-makers’: Negative Existentials,” in Lillehammer & Rodriguez-Pereyra (eds.) 2003: 39–41."
    p13 = regbibparser.parseitem(i13)
    assert 'David Lewis and Gideon Rosen' == p13['author']

    i14 = u"Lewis, D. and S. Lewis, 1970, “Holes,” Australasian Journal of Philosophy, 48: 206–212."
    p14 = regbibparser.parseitem(i14)
    assert 'D. Lewis and S. Lewis' == p14['author']

    i15 = u"Hardy, J. D., H. J. Wolff and H. Goodell (1952). <em>Pain Sensations and Reactions</em>. Baltimore, MD: Williams and Wilkins."
    p15 = regbibparser.parseitem(i15)
    assert 'J.D. Hardy, H. J. Wolff and H. Goodell' == p15['author']

    i16 = u"Jevons, W. S. [1858]. The Social Cesspools of Sydney No. 1. — The Rocks. <em>The Sydney Morning Herald</em>, October 7, 1858, typescript provided by Michael V. White."
    p16 = regbibparser.parseitem(i16)
    assert 'W.S. Jevons' == p16['author']
    assert 1858 == p16['year']

    i17 = u'<font color="gray">[Loeb edition with English translation.]</font>'
    p17 = regbibparser.parseitem(i17)
    assert p17 is None

    i18 = u"Dover, K[enneth] J. 1968, <em>Aristophanes: Clouds</em>, Oxford: Clarendon Press."
    p18 = regbibparser.parseitem(i18)
    assert 1968 == p18['year']
    assert 'Kenneth J. Dover' == p18['author']

    i19 = u"Barnes, J. [O. Testudo, pseud.], 1981, “Space for Zeno,” <em>Deucalion</em>, 33/34: 131–45. J."
    p19 = regbibparser.parseitem(i19)
    assert 1981 == p19['year']
    assert 'J. Barnes' == p19['author']

    i20 = u"<li>Jackson, Frank ed. 1991: <em>Conditionals</em>. Oxford: Clarendon"
    p20 = regbibparser.parseitem(i20)
    assert 1991 == p20['year']
    assert 'Frank Jackson (ed.)' == p20['author']

    i21 = u"Braun, D.,1993, “Empty Names”, Noûs, 27: 449–69."
    p21 = regbibparser.parseitem(i21)
    assert 1993 == p21['year']
    assert 'D. Braun' == p21['author']
