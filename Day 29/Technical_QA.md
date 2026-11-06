# ShopEase – Technical Interview Questions & Answers

## 1. What is ShopEase?

ShopEase is an AI-powered customer support chatbot designed for
e-commerce platforms. It helps customers get information about
products, shipping, returns, refunds and other common support queries.

It combines a web-based chat interface, a FastAPI backend and a
LangGraph-based multi-agent workflow to process customer queries.
It also supports conversation context and escalation when automated
assistance is insufficient.

## 2. What problem does ShopEase solve?

E-commerce businesses receive repetitive customer queries about
products, orders, delivery and return policies. Handling every query
manually can increase support workload and response time.

ShopEase aims to automate routine customer interactions, provide
relevant information and offer a human-support escalation mechanism
when necessary.

## 3. Why did you use LangGraph?

LangGraph helps organise an AI application into a structured workflow
of connected processing steps.

Instead of handling the entire query through one large function,
ShopEase uses specialised agents for different responsibilities,
such as retrieving information, analysing the query, generating
a response and checking its relevance.

This makes the workflow easier to organise, understand and extend.

## 4. How does the multi-agent architecture work?

The application follows a coordinated workflow:

1. The customer submits a query through the frontend.
2. The backend receives and processes the query.
3. The research component retrieves relevant information.
4. The analysis component evaluates the retrieved information
   and determines whether additional support is required.
5. The response-generation component prepares an answer.
6. The review component checks the response.
7. The final response is returned to the customer.

The components work together rather than operating as independent
chatbots.

## 5. How is product information retrieved?

ShopEase integrates the DummyJSON Products API to retrieve
sample product catalogue information.

The integration can provide information such as:

- Product names
- Descriptions
- Prices
- Categories
- Availability information
- Search results

Using an external API allows the application to retrieve product
information without maintaining an entire product catalogue locally.

**Important:** DummyJSON provides sample data and is not connected
to a real e-commerce inventory.

## 6. What is the purpose of the knowledge base?

The knowledge base stores predefined customer-support information
in a structured local JSON file.

It contains support articles covering topics such as:

- Delayed deliveries
- Returns and refunds
- Contacting support
- Order cancellation

The research component searches this information to find relevant
content for customer queries.

This helps the chatbot provide answers based on predefined
support information instead of generating every answer without
a reference.

## 7. How does conversation memory work?

Conversation memory allows the chatbot to retain relevant
conversation context during a session.

For example:

Customer: Tell me about wireless headphones.

Customer: What about their price?

The second question can be interpreted using the context of the
first question rather than treating it as a completely unrelated
query.

The implementation uses session-based conversation context.
It should not be confused with permanent user memory across
different sessions.

## 8. What happens when the chatbot cannot resolve a query?

ShopEase includes a human-support escalation mechanism.

When the system determines that a query requires additional
assistance, it can direct the customer towards escalation and
create a support request.

The demo implementation stores ticket information locally.

It does not represent a live connection to an actual customer
support team or ticket-management platform.

## 9. What technologies are used in ShopEase?

The major technologies and components include:

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| FastAPI | Backend API development |
| LangGraph | Multi-agent workflow coordination |
| DummyJSON API | Sample product catalogue |
| JSON | Local knowledge base and demo ticket storage |
| HTML | Frontend structure |
| CSS | Frontend styling |
| JavaScript | Frontend interactions |

Each component contributes to a particular part of the application.

## 10. What are the current limitations and future improvements?

### Current Limitations

- DummyJSON provides sample product information rather than
  real inventory data.
- The knowledge base contains a limited collection of predefined
  support articles.
- Support tickets are stored locally rather than being assigned
  to actual support representatives.
- Session-based context is not equivalent to persistent
  cross-session memory.
- The system depends on the availability of external product
  API services for product retrieval.

### Future Improvements

- Integrate a real e-commerce product and order-management API.
- Expand the knowledge base with more detailed support articles.
- Introduce persistent conversation history.
- Connect escalation requests to a real ticket-management system.
- Add authentication and customer-specific support history.
- Improve retrieval accuracy using semantic search.
- Deploy the application on a production hosting platform.

---

## Quick Revision

| Topic | Key Point |
|---|---|
| Project | AI-powered e-commerce support chatbot |
| Backend | FastAPI |
| Workflow | LangGraph multi-agent architecture |
| Product Data | DummyJSON API |
| Support Information | Local JSON knowledge base |
| Memory | Session-based conversation context |
| Escalation | Local demo support-ticket creation |
| Frontend | HTML, CSS and JavaScript |

## Interview Tip

While explaining ShopEase, focus on three things:

1. **Architecture:** Explain how the different agents cooperate.
2. **Implementation:** Explain how product retrieval, support
   information and conversation context are handled.
3. **Practical Value:** Explain how automation reduces repetitive
   customer-support work while retaining an escalation option.

Be clear about what is implemented, what is simulated and what
could be improved in a production version.