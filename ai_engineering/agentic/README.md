# Agentic AI

<div style="float: right; width: 220px; background: #f5f5f5; padding: 15px; border-radius: 5px; margin-left: 20px;">

**Learning Materials**
- [LLM Course](../llm/README.md)
- [RAG Guide](../rag/README.md)
- **Agentic AI** ← You are here

</div>

This directory contains notes and examples on building AI agents - systems where LLMs coordinate tools and take autonomous actions.

## Topics to Cover

- [ ] Agent architecture and loops
- [ ] Tool definitions and schemas
- [ ] Model Context Protocol (MCP)
- [ ] Agent-to-Agent communication
- [ ] Multi-agent orchestration
- [ ] ReAct (Reasoning + Acting) framework
- [ ] Planning and decomposition
- [ ] Error handling and recovery
- [ ] Security: tool permissions and sandboxing
- [ ] Human-in-the-loop for high-risk actions
- [ ] Agent evaluation and testing

## Why Agents Matter

- **Multi-step autonomy**: Accomplish complex tasks without human intervention at each step
- **Tool coordination**: Seamlessly integrate code execution, web search, database queries
- **Scalability**: One agent can delegate to specialized sub-agents
- **Real-world grounding**: Actions have consequences; agents learn to verify

## Agent vs Chatbot vs Copilot

| Type | Autonomy | Example |
|------|----------|---------|
| **Chatbot** | User submits prompt; model responds | ChatGPT, Claude web interface |
| **Copilot** | Suggests next action; human executes | GitHub Copilot (code completion) |
| **Agent** | Multi-step autonomous execution | Langchain agents, Claude with tools |

Coming soon: Architecture patterns, tool design, multi-agent frameworks.
