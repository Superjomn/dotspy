"""HTML utilities for converting markdown to DOT HTML-like labels."""

from typing import Any, Dict
try:
    import mistune
    MISTUNE_AVAILABLE = True
except ImportError:
    MISTUNE_AVAILABLE = False


class DotHTMLRenderer(mistune.HTMLRenderer):
    """Custom mistune renderer that outputs DOT-compatible HTML."""
    
    def strong(self, text: str) -> str:
        """Render bold text."""
        return f'<B>{text}</B>'
    
    def emphasis(self, text: str) -> str:
        """Render italic text."""
        return f'<I>{text}</I>'
    
    def strikethrough(self, text: str) -> str:
        """Render strikethrough text."""
        return f'<S>{text}</S>'
    
    def codespan(self, text: str) -> str:
        """Render inline code as monospace font."""
        # Avoid empty FONT tags which cause graphviz errors
        if not text or not text.strip():
            return text or ''
        return f'<FONT FACE="monospace">{text}</FONT>'
    
    def linebreak(self) -> str:
        """Render line break."""
        return '<BR/>'
    
    def heading(self, text: str, level: int, **attrs) -> str:
        """Render heading with appropriate font size as a table row."""
        # DOT FONT POINT-SIZE for different heading levels
        sizes = {1: 20, 2: 18, 3: 16, 4: 14, 5: 12, 6: 11}
        size = sizes.get(level, 12)
        return f'<TR><TD ALIGN="LEFT"><FONT POINT-SIZE="{size}"><B>{text}</B></FONT></TD></TR>'
    
    def paragraph(self, text: str) -> str:
        """Render paragraph as a table row."""
        # Remove trailing whitespace
        text = text.rstrip()
        if text:
            return f'<TR><TD ALIGN="LEFT">{text}</TD></TR>'
        return ''
    
    def newline(self) -> str:
        """Render newline."""
        return '<BR/>'
    
    def list(self, text: str, ordered: bool, **attrs) -> str:
        """Render list using nested TABLE structure as a table row."""
        # Wrap list items in a nested table, then wrap that in a table row
        return f'<TR><TD><TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="2">{text}</TABLE></TD></TR>'
    
    def list_item(self, text: str, **attrs) -> str:
        """Render list item with bullet or number."""
        # Use bullet point for unordered lists
        # Note: We don't have easy access to whether it's ordered here
        # so we'll use a bullet by default
        bullet = '&#8226; '  # bullet character
        return f'<TR><TD ALIGN="LEFT">{bullet}{text}</TD></TR>'
    
    def table(self, text: str) -> str:
        """Render table as a nested table inside a table row."""
        return f'<TR><TD><TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">{text}</TABLE></TD></TR>'
    
    def table_head(self, text: str) -> str:
        """Render table head - wraps header cells in TR."""
        return f'<TR>{text}</TR>'
    
    def table_body(self, text: str) -> str:
        """Render table body."""
        return text
    
    def table_row(self, text: str) -> str:
        """Render table row."""
        return f'<TR>{text}</TR>'
    
    def table_cell(self, text: str, align: str = None, head: bool = False, **kwargs) -> str:
        """Render table cell."""
        attrs = []
        if align:
            attrs.append(f'ALIGN="{align.upper()}"')
        
        attrs_str = ' ' + ' '.join(attrs) if attrs else ''
        
        if head:
            text = f'<B>{text}</B>'
        
        return f'<TD{attrs_str}>{text}</TD>'
    
    def link(self, text: str, url: str, title: str = None) -> str:
        """Render link - DOT doesn't support hyperlinks in labels, so just show text."""
        # We could potentially use URL attribute on node, but in label just show text
        return text
    
    def image(self, alt: str, url: str, title: str = None) -> str:
        """Render image - DOT doesn't support images in HTML labels, show alt text."""
        return f'[{alt}]' if alt else '[image]'
    
    def block_code(self, code: str, info: str = None) -> str:
        """Render code block as a nested table inside a table row."""
        # Use table with monospace font for code blocks
        lines = code.rstrip().split('\n')
        # Avoid empty FONT tags - if line is empty, use a space
        rows = ''.join(
            f'<TR><TD ALIGN="LEFT"><FONT FACE="monospace">{line if line.strip() else " "}</FONT></TD></TR>' 
            for line in lines
        )
        return f'<TR><TD><TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="2">{rows}</TABLE></TD></TR>'
    
    def block_quote(self, text: str) -> str:
        """Render block quote as a nested table inside a table row."""
        # Block quotes contain indented content
        # The text contains table rows from nested paragraphs
        # We need to wrap them in a TABLE, then indent that table
        return f'<TR><TD><TABLE BORDER="0" CELLBORDER="0"><TR><TD WIDTH="20"></TD><TD ALIGN="LEFT"><TABLE BORDER="0" CELLBORDER="0">{text}</TABLE></TD></TR></TABLE></TD></TR>'
    
    def thematic_break(self) -> str:
        """Render thematic break (horizontal rule) as a table row."""
        # DOT doesn't have HR, use a line of dashes in a table row
        return '<TR><TD ALIGN="LEFT">──────────────────</TD></TR>'


def markdown_to_dot_html(markdown_text: str) -> str:
    """
    Convert markdown text to DOT HTML-like label syntax.
    
    Args:
        markdown_text: Markdown formatted text
        
    Returns:
        DOT-compatible HTML string wrapped in a master table
        
    Raises:
        ImportError: If mistune is not installed
    """
    if not MISTUNE_AVAILABLE:
        raise ImportError(
            "mistune is required for markdown support. "
            "Install it with: pip install 'dotspy[html]' or pip install mistune>=3.0"
        )
    
    # Create markdown parser with custom renderer and plugins
    renderer = DotHTMLRenderer()
    md = mistune.create_markdown(
        renderer=renderer,
        plugins=['strikethrough', 'table', 'url']
    )
    
    # Convert markdown to HTML - each block becomes a TR
    html = md(markdown_text)
    
    # Clean up any extra whitespace
    html = html.strip()
    
    # Wrap all content in a master table
    # This ensures DOT sees a single TABLE root element
    # BORDER="0" makes the master table invisible, showing only the content
    if html:
        html = f'<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">{html}</TABLE>'
    
    return html

