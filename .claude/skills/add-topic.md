# Add New Topic/Chapter

## Description
Streamlined workflow for adding new topics, chapters, or markdown files to your learning materials. Automatically updates the reader navigation, maintains organization, and commits changes.

## When to use
- Adding a new topic section (e.g., "Advanced RAG", "Fine-tuning")
- Adding chapters to existing topics (e.g., new embeddings guide)
- Adding supporting files (notes, examples, quick references)

## How it works

### Step 1: Collect information
Gather details about what you're adding:
- **Topic section**: Where does this belong? (LLM, Embeddings, Vector DB, RAG, Agentic, or NEW)
- **File path**: Where in the repo? (e.g., `ai_engineering/llm/06_advanced_prompting.md`)
- **Title**: Human-readable name (e.g., "Advanced Prompting Techniques")
- **Is primary topic**: Is this a main section header or a subtopic?

### Step 2: Add the markdown file
If it's a new file, create it with:
```bash
# Create new chapter
echo "# Your Title\n\nContent here..." > path/to/file.md
```

Or provide existing markdown content.

### Step 3: Update reader.html
The skill will:
1. Find the chapters array in `reader.html`
2. Add your new chapter in the correct section
3. Maintain alphabetical/logical ordering
4. Format consistently with existing entries

### Step 4: Test
```bash
# Start local server if not running
python3 -m http.server 3000

# Visit: http://localhost:3000/reader.html
# Verify your chapter appears in sidebar and is clickable
```

### Step 5: Commit
```bash
git add .
git commit -m "feat: add [topic] - [description]"
git push
```

## Chapter array format
Each chapter entry looks like:
```javascript
{ title: 'Chapter Name', file: 'ai_engineering/section/filename.md', section: 'Section Name' },
```

**Important:**
- `title`: Display name in sidebar
- `file`: Full path from repo root, forward slashes
- `section`: Grouped navigation header (Overview, LLM, Embeddings, Vector DB, RAG, Agentic, etc.)

## Common patterns

### Adding a subtopic to existing section
```javascript
// After README.md for that section
{ title: 'Your Chapter', file: 'ai_engineering/llm/06_your_file.md', section: 'LLM' },
```

### Creating a completely new topic section
```javascript
// Create directory structure
ai_engineering/newtopic/
├── README.md
├── 00_guide.md
└── 01_examples.md

// Add to chapters array
{ title: 'New Topic', file: 'ai_engineering/newtopic/README.md', section: 'New Topic' },
{ title: 'Guide', file: 'ai_engineering/newtopic/00_guide.md', section: 'New Topic' },
{ title: 'Examples', file: 'ai_engineering/newtopic/01_examples.md', section: 'New Topic' },
```

### Organizing within a section
Number your files for logical ordering:
```
00_topic_guide.md          (Main guide)
01_practical_examples.md   (How to use)
02_quick_reference.md      (Cheat sheet)
03_advanced_techniques.md  (Deep dive)
```

## Files modified
- `reader.html` — chapters array updated

## After running
The reader will automatically:
- Show new chapters in sidebar
- Organize them under correct section
- Enable navigation between all chapters
- Support internal markdown links

## Tips
- Keep `title` concise but descriptive
- Use consistent file naming (00_, 01_, 02_ prefixes for ordering)
- Test by clicking through adjacent chapters to verify next/prev navigation
- Markdown links inside chapters will automatically route through reader
