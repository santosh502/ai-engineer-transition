# AI Engineer Transition - Project Guide

## Project Overview
An interactive learning hub for the 18-week AI engineering transition program with beautiful markdown viewer, chapter navigation, and organized learning materials.

## Directory Structure

```
.
├── index.html                 # Main hub/dashboard
├── reader.html               # Universal markdown reader with navigation
├── viewer.html               # Alternative markdown viewer (legacy)
├── ai_engineering/
│   ├── README.md            # Overview
│   ├── llm/                 # Large Language Models
│   │   ├── README.md
│   │   ├── 00_attention...md
│   │   ├── 01_llm_fundamentals.md
│   │   ├── 02_practical_examples.md
│   │   └── ...
│   ├── embeddings/          # Text embeddings & vectors
│   │   ├── README.md
│   │   ├── 00_embeddings_guide.md
│   │   ├── 01_practical_code_examples.md
│   │   └── 02_quick_reference.md
│   ├── vector_databases/    # Vector search & storage
│   ├── rag/                 # Retrieval-Augmented Generation
│   └── agentic/             # Agentic AI systems
├── projects/                # Hands-on projects
├── ai_engineering_*.py      # Supporting scripts
└── .claude/
    └── skills/
        └── add-topic.md     # Guide for adding new chapters
```

## Key Files

### `index.html`
- Main dashboard & hub
- Links to learning materials and projects
- Quick access cards and stats

### `reader.html`
**The universal markdown viewer** with:
- 21+ chapters organized in 5 topic sections
- Full chapter navigation (sidebar + next/prev buttons)
- Syntax highlighting with copy buttons
- Keyboard shortcuts (← →)
- Internal link rewriting (markdown links route through reader)

**To add chapters, edit the `chapters` array in reader.html**

### Markdown Files
- Store all content in `ai_engineering/[topic]/`
- Name files with `00_`, `01_`, `02_` prefixes for ordering
- Each main topic should have a `README.md`

## Adding New Content

### Quick: Add a chapter to existing topic
1. Create markdown file in existing topic dir
2. Add entry to `chapters` array in `reader.html`
3. Test at http://localhost:3000/reader.html
4. Commit

**Example:**
```javascript
{ title: 'Your Chapter', file: 'ai_engineering/llm/06_new_file.md', section: 'LLM' },
```

See `/skill add-topic` for detailed guide.

### Full: Create new topic section
1. Create directory: `ai_engineering/newtopic/`
2. Create `README.md` with overview
3. Add supporting files (guides, examples, references)
4. Add all to `chapters` array in `reader.html`
5. Group under new section name

## Development

### Start local server
```bash
python3 -m http.server 3000
# Visit http://localhost:3000/
```

### File changes to track
- Markdown files (`.md`) - content
- `reader.html` - chapters array only
- No other HTML files need updating

### Testing
- Click through chapters in sidebar
- Verify next/prev navigation works
- Test internal markdown links (notes.md, examples.md, etc.)
- Check syntax highlighting on code blocks

## Deployment
- GitHub Pages automatic on push to main
- Site: https://santosh502.github.io/ai-engineer-transition/

## Conventions

### File naming
```
00_topic_guide.md           # Main guide/overview
01_practical_examples.md    # How-to with code
02_quick_reference.md       # Cheat sheet
03_advanced_techniques.md   # Deep dives (if needed)
```

### Chapter array
```javascript
{ 
  title: 'Display Name',              // Shown in sidebar
  file: 'path/from/repo/root.md',     // Full path, forward slashes
  section: 'Topic Section'            // Grouping header
}
```

### Markdown structure
```markdown
# Main Title

Brief intro paragraph.

## Section 1
Content...

## Section 2
Content...
```

## Common Tasks

### View specific chapter
http://localhost:3000/reader.html?file=ai_engineering/embeddings/00_embeddings_guide.md

### Keyboard shortcuts in reader
- `←` Arrow Left: Previous chapter
- `→` Arrow Right: Next chapter
- Click section headers to expand/collapse

### Reorder chapters
Edit `chapters` array in `reader.html` - order determines navigation sequence.

## Technology Stack
- HTML5 / CSS3 / Vanilla JavaScript
- **markdown-it** - Markdown parsing
- **highlight.js** - Code syntax highlighting
- **IBM Plex fonts** - Typography
- Dark theme with cyan accent (#5eead4)

## Notes
- All chapters must have `.md` extension
- Paths in `chapters` array are relative to repo root
- Internal `.md` links automatically rewrite to reader URLs
- Code blocks auto-highlight with "Copy" button
