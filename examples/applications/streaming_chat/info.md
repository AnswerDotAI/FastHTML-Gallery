# Async Streaming Chat (OpenAI, Llamaindex)

This project is a web-based streaming chat app built using FastHTML, HTMX, Llamaindex, DaisyUI, and the OpenAI API. It handles real-time chat communication using WebSocket streaming in asyc mode.

- An OpenAI API key is required to run this demo. The API key is set via a form and stored in the session for the duration of the chat.

## Key Technologies and Techniques

1. **FastHTML**: Creates server-side logic and HTML components.  
2. **HTMX**: Dynamically updates chat messages without full page reloads.  
3. **OpenAI API**: Provides AI-powered chat responses.  
4. **Llamaindex**: Adds RAG capabilities to Open AI chaat.  
5. **DaisyUI**: Adds prestyled, robust UI components.  
6. **WebSocket Streaming**: Streams AI responses in real-time.

## How It Works

### Server-Side Logic

- `app.py` manages chat sessions, processes user messages via OpenAI, and retains conversation state in memory.
- WebSocket streaming enables partial updates to the chat interface as the assistant response is generated asynchronously.

### Dynamic Content

- Message chunks from OpenAI agent are received in async mode and are sent to the client as they are generated, updating the chat interface in real-time.  
- Content is dynamically updated to MD format line-by-line, with each line displayed as it is received.
- HTMX triggers updates with minimal overhead, refreshing parts of the page on demand.

### Key Features

1. **Incremental Streaming**: Partial responses are sent in WebSocket chunks asynchronously.  
2. **Conversation Persistence**: Each user's chat data is stored in a session dictionary.  
3. **DaisyUI Styling**: Offers clean, consistent UI elements without extensive CSS.  
4. **Llamaindex**: Processes and indexes conversation context for improved query handling.  
5. **Markdown Rendering**: Generated answers are displayed in rich text format.
6. **OpenAI API Key Requirement**: An OpenAI API key is required to run this demo, which is set via a form and stored in the session.