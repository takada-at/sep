# coding:utf-8
from pyparsing import Literal, Regex, Word, alphas, alphanums, nums, printables, Or, ZeroOrMore, delimitedList

u"""
<li>Smith, Michael, 2003. &ldquo;Rational Capacities,&rdquo; in Stroud and Tappolet (eds.), <em>Weakness of Will and Practical Irrationality</em>, Oxford: Oxford University Press: 17&ndash;38.</li>
<li>Adler, J., 1994. &ldquo;Testimony, Trust, Knowing,&rdquo; <em>Journal of Philosophy</em>, 91: 264&ndash;275.</li>

<li>Wilks, Ian. (1993) <em>The Logic of Abelard's Dialectica</em>. Doctoral Dissertation in Philosophy, the University of Toronto.</li>
<li>Wilks, Ian. (1997) “The Role of Virtue Theory and Natural Law in Abelard's Ethical Writings” in <em>Proceedings of the American Catholic Philosophical Association</em> 71: 137–149.</li>

<li>[A] <em>Aṅguttara-nikāya</em></li>

<li>Conze, E., 1962, <em>Buddhist Thought in India: Three Phases of Buddhist Philosophy</em>, London: George Allen &amp; Unwin.</li>
<li>Cousins, L., 1981, “The <em>Paṭṭhāna</em> and the Development of the Theravādin Abhidhamma,” <em>Journal of the Pali Text Society</em>, 9: 22–46 .</li>
<li>&ndash;&ndash;&ndash;, 2007, &ldquo;Copernicus and His Islamic Predecessors,&rdquo; <em>History of Science</em>, 45: 65&ndash;81.</li>



<li>Barnes, J., ed. <em>The Complete Works of Aristotle</em>, Volumes I and II, Princeton: Princeton University Press, 1984.</li>
<li>Gershenzon, Shoshanna. 2000. “Myth and Scripture: the <em>Dialoghi d'Amore</em> of Leone Ebreo.” <em>A Crown for a King</em>: 125–145.</li>
<li>–––. 2011. <i>Alone Together: Why We Expect More From Technology and Less From Each Other</i>. New York: Basic Books.</li>
<li>Wilks, Ian. (1998) “Peter Abelard and the Metaphysics of Essential Predication” in <em>Journal of the History of Philosophy</em> 36: 356–385.</li>
"""
booktagl = Or(Literal('<em>'), Literal('<i>'))
booktagr = Or(Literal('</em>'), Literal('</i>'))
litagl = Literal('<li>').suppress()
litagr = Literal('</li>').suppress()
lparen = Literal('(').suppress()
rparen = Literal(')').suppress()
lquote = Literal(u'“').suppress()
rquote = Literal(u'“').suppress()
shortname = (Literal('[') + Word(alphas) + Literal(']')).suppress()

dot = Literal('.').suppress()
space = Literal(' ').suppress()
comma = Literal(',').suppress()
sep = Or(comma, dot)
inlit = Literal('in').suppress()
edlit = Literal('ed.').suppress()

nameparts = Word(alphas + '.')
author = nameparts + comma + nameparts
publisher = Word(alphanums + ' ')
year = Regex(r'\(?[0-9]{4,4}\)?')
ignore = Regex('.*').suppress()
bookname = booktagl + Word(printables) + booktagr
papername = lquote + Word(printables) + ZeroOrMore(comma) + rquote
vol = Word(printables)

paper0 = author + sep + year + sep + papername + inlit + ignore
book0 = author + sep + year + sep + bookname + sep + publisher + dot
book1 = author + lparen + year + rparen + bookname + sep + publisher + dot
paper1 = author + lparen + year + rparen + inlit + space + bookname + vol + dot
book2 = author + year + sep + bookname + sep + publisher + dot
paper2 = author + year + sep + papername + space + bookname + sep + vol + dot
bookshort = shortname + space + bookname

book = Or(Or(Or(book0, book1), book2), bookshort)
paper = Or(Or(paper0, paper1), paper2)

bibitem = Or(book, paper)
