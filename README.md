# Test EMR (training site): fictional patients only

**This is not a real medical record system.** It is a small static website for testing software: for example, a
bot that signs in, finds a patient, reads the summary and adds a comment. All 100 patients, and every name, date of
birth, chart number, insurance ID and clinical detail on the site, are fictional (`data/patients.json`, made by
`tools/make_patients.py`). Any resemblance to real people is coincidental.

- **Sign in:** user name `authorization`, password `hello`. This is a practice step for the software being tested,
  not security; the site is public and has nothing to protect.
- **Patient list:** 100 fictional retina patients, searchable by name, chart # or date of birth.
- **Summary page:** a generic EMR-style summary (patient banner, problems, eye measurements, medications, prior
  authorizations, injections, visits) with a yellow Comments panel.
- **Comments:** click **Comment**, type, then **Save comment**. Comments are stored only in the browser that
  wrote them (localStorage); nothing is sent anywhere.

Element ids for automation: `#username`, `#password`, `#signin`, `#search`, `.patient-link`, `#patient-header`,
`#hdr-name`, `#hdr-dob`, `#hdr-mrn`, `#prior-auths`, `#add-comment`, `#comment-text`, `#save-comment`,
`#comment-list`, `#signout`.

No trackers, no external scripts or fonts, no cookies.
