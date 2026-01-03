Business Rules:



Orders

* order\_id is unique
* purchase timestamp exists
* status is valid



Order Items

* price > 0
* order\_id exists in orders



Payments

* payment\_value >= 0



Marketing Spend

* spend\_amount >= 0
* date is not null



Refunds

* refund\_amount <= order\_amount
* refund\_date > order\_purchase\_date
