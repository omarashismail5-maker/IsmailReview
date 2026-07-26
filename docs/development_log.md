Day 4: 7/17/2026

###

testIdentification_1: Tests for recognition of an activity description. The key word
here is "Played"

Input: "Played in intramural volleyball for some time."

Expected Output: "Input Type: Activity description"

Actual Output: "Input Type: Activity description"

Result: PASS

###

testIdentification_2: Tests for recognition of resume bullet. The key word
here is "Helped"

Input: "Helped fix machines and respond to questions."

Expected Output: "Input Type: Resume bullet"

Actual Output: "Input Type: Resume bullet"

Result: PASS

###

testIdentification_3: Tests for recognition of a short answer. The key here is 
the length of the input, but also key words like "I would" and "I believe"

Input: "I would like to join this program because I believe that my experience, attitude, and charisma will be extremely useful for this position."

Expected Output: "Input Type: Short answer"

Actual Output: "Input Type: Short answer"

Result: PASS

Day 6: 7/21/2026

###

testCommonMistakes_1: Tests for recognition of vague words, this one is "some time"

Input: "Played in intramural volleyball for some time."

Expected Output: 
"
*Input Type*
- The draft may use vague wording: 'some time'.
- The draft may be too short to show meaningful detail.
- The draft may need a clearer impact, result, or growth statement.
*rest of the feedback*
"

Actual Output:
"
*Input Type*
- The draft may use vague wording: 'some time'.
- The draft may be too short to show meaningful detail.
- The draft may need a clearer impact, result, or growth statement.
*rest of the feedback*
"

Result: PASS

###

testCommonMistakes_2: Tests for recognition of answers that are too short.

Input: "Served my community."

Expected Output: 
"
*Input Type*
Detected Issues:
- The draft may be too short to show meaningful detail.
- The draft may need a clearer impact, result, or growth statement.
*rest of the feedback*
"

Actual Output:
"
*Input Type*
Detected Issues:
- The draft may be too short to show meaningful detail.
- The draft may need a clearer impact, result, or growth statement.
*rest of the feedback*
"
Result: PASS

###

Day 7: 7/26/2026

testBasicCLassification: Tests for recognition of answers that are essays.

Input: "I really like working at my college gym because it is fun and I enjoy helping people."

Expected Output: 
"
Detected Input Type: essay
*rest of the feedback*
"

Actual Output:
"
Detected Input Type: Short answer
*rest of the feedback*
"
Result: FAIL

---

New Input: "Rock climbing initially interested me because it combined physical challenge with problem-solving. Over time, however, injuries forced me to reconsider how I approached the sport. During recovery, I learned patience, proper technique, and the importance of supporting other climbers. Returning to climbing eventually allowed me to develop skills in belaying, rappelling, and rescue procedures while becoming a more responsible member of the climbing community."

Expected Output: 
"
Detected Input Type: essay
*rest of the feedback*
"

Actual Output:
"
Detected Input Type: Short answer
*rest of the feedback*
"
Result: FAIL

---

*Code Updated*

New Input: "Rock climbing initially interested me because it combined physical challenge with problem-solving. Over time, however, injuries forced me to reconsider how I approached the sport. During recovery, I learned patience, proper technique, and the importance of supporting other climbers. Returning to climbing eventually allowed me to develop skills in belaying, rappelling, and rescue procedures while becoming a more responsible member of the climbing community."

Expected Output: 
"
Detected Input Type: essay
*rest of the feedback*
"

Actual Output:
"
Detected Input Type: essay
*rest of the feedback*
"
Result: PASS