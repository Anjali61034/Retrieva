# Transaction Event Schema

| Field                  | Type      | Nullable | Notes                                              |
|-------------------------|-----------|----------|-----------------------------------------------------|
| transaction_id           | string    | No       | Unique ID, e.g. "txn_00001"                        |
| merchant_id               | string    | No       | e.g. "merch_01" to "merch_05" (simulate 5 merchants) |
| amount                    | float     | No       | In ₹, range e.g. 50–50000                          |
| payment_method            | string    | No       | One of: card, upi, netbanking, wallet              |
| timestamp_initiated        | datetime  | No       | When checkout started                              |
| timestamp_otp_sent         | datetime  | Yes      | Null if OTP step never reached                     |
| timestamp_next_event       | datetime  | Yes      | Null if session just died (network drop case)      |
| error_code                 | string    | Yes      | e.g. "TIMED_OUT", "INSUFFICIENT_FUNDS", null       |
| status                     | string    | No       | One of: success, failed, abandoned                 |
| user_id                    | string    | No       | For per-user daily discount cap tracking later      |