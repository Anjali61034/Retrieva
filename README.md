# Retrieva

AI agent that detects, diagnoses, and recovers failed or abandoned checkouts on Razorpay test-mode payment data.

Retrieva classifies each failed/abandoned transaction into one of five causes (OTP timeout, bank/gateway timeout, insufficient funds, payment-method mismatch, network drop), maps each cause to a bounded recovery action (retry nudge, alternate-method suggestion, or no action), and logs every decision to an append-only audit trail.

## Status
Work in progress — built for Razorpay AI Buildathon 2026, Track 03 (AI Revenue Recovery).