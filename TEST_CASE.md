Test Case: Batch Resume Upload with One Invalid Resume

Objective

Verify that one invalid resume does not stop the processing of the remaining resumes.

Test Data

* GoodResume.pdf
* bad_resume.pdf (corrupted PDF)
* GoodResume.docx

Steps

1. Open the Talent Pool Search application.
2. Select all three resumes.
3. Click Upload Resumes.
4. Wait for the upload process to complete.

Expected Result

* GoodResume.pdf is processed successfully.
* GoodResume.docx is processed successfully.
* bad_resume.pdf is not processed.
* The application continues processing the remaining resumes.
* The UI displays the failed filename with a user-friendly error message.
* The successfully processed resumes are saved to the database.

Actual Result

The application processed the two valid resumes successfully. The corrupted PDF failed with the message “Invalid or corrupted PDF file.” The application continued processing without stopping, and the valid resumes were saved successfully.

Status

PASS