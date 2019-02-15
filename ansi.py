raw = """0 	Reset / Normal 	all attributes off
1 	Bold or increased intensity 	
2 	Faint (decreased intensity) 	
3 	Italic 	Not widely supported. Sometimes treated as inverse.
4 	Underline 	
5 	Slow Blink 	less than 150 per minute
6 	Rapid Blink 	MS-DOS ANSI.SYS; 150+ per minute; not widely supported
7 	reverse video 	swap foreground and background colors
8 	Conceal 	Not widely supported.
9 	Crossed-out 	Characters legible, but marked for deletion.
10 	Primary(default) font 	
11–19 	Alternative font 	Select alternative font n − 10 {\displaystyle n-10} {\displaystyle n-10}
20 	Fraktur 	Rarely supported
21 	Doubly underline or Bold off 	Double-underline per ECMA-48.[22] See discussion
22 	Normal color or intensity 	Neither bold nor faint
23 	Not italic, not Fraktur 	
24 	Underline off 	Not singly or doubly underlined
25 	Blink off 	
27 	Inverse off 	
28 	Reveal 	conceal off
29 	Not crossed out 	
30–37 	Set foreground color 	See color table below
38 	Set foreground color 	Next arguments are 5;n or 2;r;g;b, see below
39 	Default foreground color 	implementation defined (according to standard)
40–47 	Set background color 	See color table below
48 	Set background color 	Next arguments are 5;n or 2;r;g;b, see below
49 	Default background color 	implementation defined (according to standard)
51 	Framed 	
52 	Encircled 	
53 	Overlined 	
54 	Not framed or encircled 	
55 	Not overlined 	
60 	ideogram underline or right side line 	Rarely supported
61 	ideogram double underline or double line on the right side
62 	ideogram overline or left side line
63 	ideogram double overline or double line on the left side
64 	ideogram stress marking
65 	ideogram attributes off 	reset the effects of all of 60–64
90–97 	Set bright foreground color 	aixterm (not in standard)
100–107 	Set bright background color 	aixterm (not in standard)
#3 	Double-height letters, top half 	DECDHL
#4 	Double-height letters, bottom half 	DECDHL
#5 	Single width, single height letters 	DECSWL
#6 	Double width, single height letters 	DECDWL"""

seqs = []
for line in raw.split('\n'):
    row = line.strip().split('\t')
    seq = row[0].strip()
    desc = row[1].strip()
    if '–' in seq:  # This is an en dash, not a hyphen
        a, b = map(int, seq.split('–'))
        for n in range(a, b + 1):
            seqs.append([str(n), desc])
    else:
        seqs.append([seq, desc])
for seq, desc in seqs:
    if not seq.startswith('#'):
        seq = '[' + seq + 'm'
    print(f'\x1b{seq}{seq} : {desc}\x1b[0m')
