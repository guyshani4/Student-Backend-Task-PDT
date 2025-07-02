# Custom Status Codes

This file documents all custom status codes used in the API responses, grouped by route.

---

## /api/add-patient
- **10000** - Success: Patient added
- **10001** - Missing or empty required field
- **10002** - Invalid FirstName/LastName
- **10003** - Invalid ID
- **10004** - Invalid DateOfBirth
- **10005** - Invalid Gender
- **10006** - Invalid InterfaceLanguage
- **10999** - Internal server error

---

## /api/add-user
- **20000** - Success: User added
- **20001** - Missing or empty required field
- **20002** - Invalid UserName/FirstName/LastName
- **20003** - Invalid CreatedDate
- **20004** - Invalid PhoneNumber
- **20005** - Invalid ID
- **20006** - Invalid Email
- **20999** - Internal server error

---

## /api/setup-session
- **30000** - Success: Session added
- **30001** - Missing or empty required field
- **30002** - Invalid StartDate/EndDate
- **30003** - PatientID does not exist
- **30004** - TherapistID does not exist
- **30999** - Internal server error

---

## /api/create-report
- **40000** - Success: Report generated
- **40001** - No sessions found
- **40999** - Internal server error 