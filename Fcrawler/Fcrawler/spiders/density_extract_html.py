'''
Created on Jun 4, 2015

@author: root
'''
#coding:utf-8

import formatter
import htmllib

from cStringIO import StringIO 


class Paragraph:
    def __init__(self):
        self.text = ''
        self.bytes = 0
        self.density = 0.0
 
class LineWriter(formatter.AbstractWriter):
    def __init__(self, *args):
        self.last_index = 0
        self.lines = [Paragraph()]
        formatter.AbstractWriter.__init__(self)
 
    def send_flowing_data(self, data):
        # Work out the length of this text chunk.
        t = len(data)
        # We've parsed more text, so increment index.
        self.index += t
        # Calculate the number of bytes since last time.
        b = self.index - self.last_index
        self.last_index = self.index
        # Accumulate this information in current line.
        l = self.lines[-1]
        l.text += data
        l.bytes += b
 
    def send_paragraph(self, blankline):
        """Create a new paragraph if necessary."""
        if self.lines[-1].text == '':
            return
        self.lines[-1].text += '\n' * (blankline+1)
        self.lines[-1].bytes += 2 * (blankline+1)
        self.lines.append(Paragraph())
#         self.lines.append(Writer.Paragraph())
 
    def send_literal_data(self, data):
        self.send_flowing_data(data)
 
    def send_line_break(self):
        self.send_paragraph(0)

    def compute_density(self):
        """Calculate the density for each line, and the average."""
        total = 0.0
        for l in self.lines:
            l.density = len(l.text) / float(l.bytes)
            total += l.density
        # Store for optional use by the neural network.
        self.average = total / float(len(self.lines))
 
    def output(self):
        """Return a string with the useless lines filtered out."""
        self.compute_density()
        output = StringIO()
        for l in self.lines:
            # Check density against threshold.
            # Custom filter extensions go here.
            if l.density >= 0.5:
                output.write(l.text)
        return output.getvalue()


class TrackingParser(htmllib.HTMLParser):
    """Try to keep accurate pointer of parsing location."""
    def __init__(self, writer, *args):
        htmllib.HTMLParser.__init__(self, *args)
        self.writer = writer
    def parse_starttag(self, i):
        index = htmllib.HTMLParser.parse_starttag(self, i)
        self.writer.index = index
        return index
    def parse_endtag(self, i):
        self.writer.index = i
        return htmllib.HTMLParser.parse_endtag(self, i)





def extract_text(html):
    # Derive from formatter.AbstractWriter to store paragraphs.
    writer = LineWriter()
    # Default formatter sends commands to our writer.
    lformatter = formatter.AbstractFormatter(writer)
    # Derive from htmllib.HTMLParser to track parsed bytes.
    parser = TrackingParser(writer, lformatter)
    # Give the parser the raw HTML data.
    parser.feed(html)
    parser.close()

    # Filter the paragraphs stored and output them.
    return writer.output()

if __name__ == '__main__':
    content='''
    <html>
    <head></head>
    <body>
        <div>
            <article>
                <p>This is a story about the life of Foo</p>
                <p>The life of Foo was one of great foo</p>
                <p>Foo foo, foo foo foo. Foo, foofoo?</p>
                <p>Foo was no stranger to foo. For Foo did foo</p>
            </article>
        </div>
        <div>
            <div>
                <p>Buy Bar Now Buy Buy Buy Buy Buy Buy Buy Buy Buy Buy Buy!</p>
                <p>Get The Bar Next Door!</p>
                <p>Increase Your Bar!</p>
                <p>Never Bar again!</p>
            </div>
        <div>
            <footer>
                <p>Who the hell is Boo. Who the hell is Far?</p
            </footer>
        </div>
    </body>
</html>
    '''
    print extract_text(content)
