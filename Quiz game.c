#include <stdio.h>

int main() {
    int answer, score = 0;

    printf("===== QUIZ GAME =====\n\n");

    // Question 1
    printf("1. Which language is used for system programming?\n");
    printf("1. HTML\n");
    printf("2. C\n");
    printf("3. CSS\n");
    printf("4. SQL\n");
    printf("Enter your answer: ");
    scanf("%d", &answer);

    if (answer == 2) {
        printf("Correct!\n\n");
        score++;
    } else {
        printf("Wrong! Correct answer is C.\n\n");
    }

    // Question 2
    printf("2. What is the full form of CPU?\n");
    printf("1. Central Processing Unit\n");
    printf("2. Computer Personal Unit\n");
    printf("3. Central Program Unit\n");
    printf("4. Control Processing Unit\n");
    printf("Enter your answer: ");
    scanf("%d", &answer);

    if (answer == 1) {
        printf("Correct!\n\n");
        score++;
    } else {
        printf("Wrong! Correct answer is Central Processing Unit.\n\n");
    }

    // Question 3
    printf("3. Which of these is an operating system?\n");
    printf("1. MS Word\n");
    printf("2. Windows\n");
    printf("3. Google\n");
    printf("4. HTML\n");
    printf("Enter your answer: ");
    scanf("%d", &answer);

    if (answer == 2) {
        printf("Correct!\n\n");
        score++;
    } else {
        printf("Wrong! Correct answer is Windows.\n\n");
    }

    // Question 4
    printf("4. Which symbol is used for comments in C?\n");
    printf("1. //\n");
    printf("2. ##\n");
    printf("3. **\n");
    printf("4. $$\n");
    printf("Enter your answer: ");
    scanf("%d", &answer);

    if (answer == 1) {
        printf("Correct!\n\n");
        score++;
    } else {
        printf("Wrong! Correct answer is //.\n\n");
    }

    // Question 5
    printf("5. Which data type is used to store an integer?\n");
    printf("1. float\n");
    printf("2. char\n");
    printf("3. int\n");
    printf("4. double\n");
    printf("Enter your answer: ");
    scanf("%d", &answer);

    if (answer == 3) {
        printf("Correct!\n\n");
        score++;
    } else {
        printf("Wrong! Correct answer is int.\n\n");
    }

    printf("===== QUIZ RESULT =====\n");
    printf("Your Score: %d/5\n", score);

    if (score == 5)
        printf("Excellent!\n");
    else if (score >= 3)
        printf("Good Job!\n");
    else
        printf("Keep Practicing!\n");

    return 0;
}
