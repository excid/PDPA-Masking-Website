# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Primary users are students and instructors evaluating a Theory of Computation assignment during a live presentation. The operational user pastes bank-system log text and needs to see personal data masked clearly and immediately.

## Product Purpose

Provide a Thai-first web interface that accepts user-entered text, applies Python regular-expression masking through the existing Django application, and returns visibly censored output. Success means the masking workflow is easy to demonstrate, the five required data types are understandable, and the presentation feels polished and creative.

## Positioning

The interface makes the regular-expression process legible: users can choose data rules, compare source and masked text, and see which categories were detected without storing submitted text.

## Operating Context

Used as a live classroom demo and as a publicly accessible assignment submission. Required data types are credit-card number, email, phone number, date of birth prefixed by `DOB:`, and address prefixed by `Address:`. The website must expose a GitHub source-code link.

## Capabilities and Constraints

- Preserve the existing Django 5, HTMX, and Alpine.js stack with no frontend build step.
- Frontend scope only: templates and static assets. Do not implement or alter regex rules, API behavior, deployment, or backend logic.
- Input is text typed or pasted by the user; output is masked text.
- Keep existing server-rendered form submission and partial updates functional.
- Support desktop presentation and responsive mobile use.
- The assignment emphasizes creative web design and presentation quality.

## Brand Commitments

- Clean, official, and easy to use; avoid theatrical or overly decorative styling.
- Use the user-approved clean compliance dashboard composition in `.impeccable/mocks/clean-compliance-a.png` as the visual quality reference.

## Evidence on Hand

- Assignment PDF: `C:\Users\Asus\Downloads\ToC Assignment 1_2569.pdf`.
- Existing skeleton, sample log, Django templates, stylesheet, and Alpine/HTMX behavior in this repository.
- No customer claims, benchmarks, testimonials, or commercial proof may be fabricated.

## Product Principles

- Make privacy transformation visible, not abstract.
- Keep the primary masking task instantly understandable.
- Preserve truthful output and backend ownership boundaries.
- Favor presentation-ready clarity without sacrificing accessibility.
- Never imply submitted text is stored; processing is in memory and discarded.

## Accessibility & Inclusion

Use semantic controls, visible focus states, sufficient contrast, keyboard operation, reduced-motion support, and responsive layouts. Thai is the primary interface language; technical identifiers may remain English where they improve precision.
