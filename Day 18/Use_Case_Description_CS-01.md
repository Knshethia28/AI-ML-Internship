# Use Case Description

## CS-01: Resolve a Customer Order Enquiry (Proposed Design, ShopEase)

| Field | Description |
|---|---|
| **Use Case ID** | CS-01 |
| **Use Case Name** | Resolve a Customer Order Enquiry |
| **Primary Actor** | Customer |
| **Supporting Components** | Customer Support AI Agent, Order Lookup Tool, Authentication Service, Human Support Team |
| **Goal** | Enable a customer to obtain accurate information about an order through an AI-assisted support conversation. |

---

### Preconditions

* The customer can access the support interface.
* The customer provides the required order information.
* The agent has access to an authorized order lookup service.
* Any required identity or ownership verification is completed before private order information is disclosed.

---

### Main Flow

1. The customer asks for an order update.
2. The agent identifies the request as an order-status enquiry.
3. The planner determines that an order lookup is required.
4. The agent validates the input and authorization requirements.
5. The agent calls the Order Lookup Tool.
6. The tool returns the available order information.
7. The agent checks the result and prepares a clear response.
8. The customer receives the response.

---

### Alternative / Error Flows

| Condition | Agent Behavior |
|---|---|
| **Missing order ID** | Ask the customer to provide the required information. |
| **Order not found** | Ask the customer to verify the details without inventing an order status. |
| **Verification failure** | Do not reveal private order information. |
| **Tool unavailable** | Explain the limitation and offer an alternative support route. |
| **Unresolved or complex issue** | Create a support ticket if the service is available and transfer the case to a human representative. |

---

### Postconditions

The customer receives a response grounded in authorized information, or the issue is routed for further assistance. The agent does not claim that a ticket was created or a handoff completed unless the relevant service confirms it.

---

### Success Criteria

* The request is classified correctly.
* Private order information is protected.
* The answer reflects the tool's actual result.
* Errors and unresolved cases are handled safely.

---

> **Status:** Design only. This use case has not been implemented or tested.
