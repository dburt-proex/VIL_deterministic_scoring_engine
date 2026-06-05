# Product Spec

## Product

Verified Intelligence Layer, or VIL, is a deterministic signal scoring and routing engine for AI-assisted operations.

## Job To Be Done

When noisy operational inputs arrive, VIL helps an operator decide which signals deserve action, review, clarification, archival, or immediate halt.

## Primary Users

- Operators managing lead intake
- Agencies handling client requests
- Contractors handling estimates and RFIs
- AI builders adding pre-execution signal quality checks
- Small teams overwhelmed by manual admin queues

## Core Promise

VIL reduces cognitive noise and creates a repeatable audit trail for why something moved forward.

## MVP Scope

Included:

- FastAPI service
- Deterministic scoring engine
- Verification cap
- Route thresholds
- Risk flag override logic
- Audit record generation
- JSON examples
- Tests
- Docker-ready deployment

Not included yet:

- Authentication
- Database persistence
- Multi-tenant dashboards
- User management
- Payment integration
- Full CASA execution governance

## Commercial Wedge

AI Workflow Intake and Risk/Value Routing Audit.

The first service install should focus on one expensive queue: leads, RFIs, support tickets, content opportunities, or internal workflow requests.
