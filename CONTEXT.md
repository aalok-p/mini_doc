# Diagnostic Test Booking

A backend service for authenticated users to book diagnostic tests at centres and complete simulated payments.

## Language

**User**:
A registered person who authenticates via JWT and books diagnostic tests for themselves. In this domain, User and Patient are the same concept.
_Avoid_: Patient, Customer, Client

**Booking**:
A reservation made by a User for a specific Diagnostic Test at a specific Diagnostic Centre on a specific date and time.
A Booking has a lifecycle status: `PENDING` (created, awaiting payment), `CONFIRMED` (payment succeeded), or `CANCELLED` (explicitly cancelled by the User).
_Avoid_: Appointment, Order, Reservation

**Booking Status**:
The state of a Booking in its lifecycle. `PENDING` means the Booking is held but not yet paid for. `CONFIRMED` means payment succeeded and the slot is secured. `CANCELLED` means the User explicitly cancelled the Booking.
_Avoid_: FAILED (this is a Payment status, not a Booking status)

**Diagnostic Centre**:
A physical location where diagnostic tests are performed.
_Avoid_: Clinic, Hospital, Lab (unless disambiguated)

**Diagnostic Test**:
A medical test or procedure offered by one or more Diagnostic Centres, with a price and duration.
_Avoid_: Service, Procedure, Product
