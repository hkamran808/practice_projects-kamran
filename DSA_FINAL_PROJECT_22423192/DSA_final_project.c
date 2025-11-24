#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "dsa_final_project.h"

int nextBlockID = 0;

int countTransactions(T_Transaction *list) {
    int count = 0;
    while (list != NULL) {
        count++;
        list = list->next;
    }
    return count;
}

T_Transaction *addTransaction(int idStud, float amount, char *descr, T_Transaction *listeTransaction) {
    T_Transaction *newTransaction = (T_Transaction *)malloc(sizeof(T_Transaction));
    if (newTransaction == NULL) {
        printf("memory allocation failed!!!\n");
        return listeTransaction;
    }
    
    newTransaction->studentID = idStud;
    newTransaction->amount = amount;
    strncpy(newTransaction->description, descr, 99);
    newTransaction->description[99] = '\0';
    newTransaction->next = listeTransaction;
    
    return newTransaction;
}

BlockChain addBlock(BlockChain bc) {
    T_Block *newBlock = (T_Block *)malloc(sizeof(T_Block));
    if (newBlock == NULL) {
        printf("memory allocation failed!!!\n");
        return bc;
    }
    
    newBlock->blockID = nextBlockID++;
    newBlock->date = getCurrentDate();
    newBlock->transactions = NULL;
    newBlock->next = bc;
    
    return newBlock;
}

float totalTransactionStudentBlock(int idStud, T_Block b) {
    float total = 0.0;
    T_Transaction *current = b.transactions;
    
    while (current != NULL) {
        if (current->studentID == idStud) {
            total += current->amount;
        }
        current = current->next;
    }
    
    return total;
}

float soldeStudent(int idStud, BlockChain bc) {
    float balance = 0.0;
    T_Block *currentBlock = bc;
    
    while (currentBlock != NULL) {
        T_Transaction *currentTransaction = currentBlock->transactions;
        while (currentTransaction != NULL) {
            if (currentTransaction->studentID == idStud) {
                balance += currentTransaction->amount;
            }
            currentTransaction = currentTransaction->next;
        }
        currentBlock = currentBlock->next;
    }
    
    return balance;
}

void credit(int idStud, float amount, char *descr, BlockChain bc) {
    if (bc == NULL) {
        printf("ERROR: no blocks in blockchain!!!\n");
        return;
    }
    
    bc->transactions = addTransaction(idStud, amount, descr, bc->transactions);
    printf("credited %.2f EATCoins to student %d\n", amount, idStud);
}

int pay(int idStud, float amount, char *descr, BlockChain bc) {
    if (bc == NULL) {
        printf("ERROR, no blocks in blockchain!!!\n");
        return 0;
    }
    
    float balance = soldeStudent(idStud, bc);
    if (balance < amount) {
        printf("NOT enough balance!!! current balance: %.2f, required: %.2f\n", balance, amount);
        return 0;
    }
    
    bc->transactions = addTransaction(idStud, -amount, descr, bc->transactions);
    printf("student %d has paid %.2f EATCoins successfully\n", idStud, amount);
    return 1;
}

void consult(int idStud, BlockChain bc) {
    float balance = soldeStudent(idStud, bc);
    printf("\n---------- student %d 's account summary ----------\n", idStud);
    printf("current balance: %.2f EATCoins\n", balance);
    printf("\nlast 5 transactions:\n");
    printf("block ID | description               | amount\n");
    printf("---------------------------------------------\n");
    
    int count = 0;
    T_Block *currentBlock = bc;
    
    while (currentBlock != NULL && count < 5) {
        T_Transaction *currentTransaction = currentBlock->transactions;
        
        while (currentTransaction != NULL && count < 5) {
            if (currentTransaction->studentID == idStud) {
                printf("%8d | %-26s | %7.2f\n", 
                       currentBlock->blockID, 
                       currentTransaction->description, 
                       currentTransaction->amount);
                count++;
            }
            currentTransaction = currentTransaction->next;
        }
        currentBlock = currentBlock->next;
    }
    
    if (count == 0) {
        printf("no transactions found for student %d\n", idStud);
    }
}

int transfer(int idSource, int idDestination, float amount, char *descr, BlockChain bc) {
    if (bc == NULL) {
        printf("ERROR: no blocks in blockchain!!!\n");
        return 0;
    }
    
    float sourceBalance = soldeStudent(idSource, bc);
    if (sourceBalance < amount) {
        printf("transfer FAILED!!! student %d does NOT have enough balance\n", idSource);
        return 0;
    }
    
    char sourceDescr[150], destDescr[150];
    snprintf(sourceDescr, 149, "transfer to %d: %s", idDestination, descr);
    snprintf(destDescr, 149, "transfer from %d: %s", idSource, descr);
    
    bc->transactions = addTransaction(idSource, -amount, sourceDescr, bc->transactions);
    bc->transactions = addTransaction(idDestination, amount, destDescr, bc->transactions);
    
    printf("%.2f EATCoins is transferred from student %d to student %d successfully!!!\n", amount, idSource, idDestination);
    return 1;
}

void exportToFile(BlockChain bc, char *filename) {
    FILE *file = fopen(filename, "w");
    if (file == NULL) {
        printf("ERROR for opening file for writing!!!\n");
        return;
    }
    
    T_Block *currentBlock = bc;
    while (currentBlock != NULL) {
        T_Transaction *currentTransaction = currentBlock->transactions;
        while (currentTransaction != NULL) {
            int year = currentBlock->date / 10000;
            int month = (currentBlock->date % 10000) / 100;
            int day = currentBlock->date % 100;
            
            fprintf(file, "%02d/%02d/%04d; %d; %.2f; %s\n",
                    day, month, year,
                    currentTransaction->studentID,
                    currentTransaction->amount,
                    currentTransaction->description);
            
            currentTransaction = currentTransaction->next;
        }
        currentBlock = currentBlock->next;
    }
    
    fclose(file);
    printf("all transactions exported to %s\n", filename);
}

BlockChain importFromFile(char *filename) {
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        printf("ERROR for opening file for reading!!!\n");
        return NULL;
    }
    
    BlockChain bc = NULL;
    char line[256];
    int currentDate = -1;
    T_Block *currentBlock = NULL;
    
    while (fgets(line, sizeof(line), file)) {
        int day, month, year, studentID;
        float amount;
        char description[100];
        
        if (sscanf(line, "%d/%d/%d; %d; %f; %99[^\n]", 
                   &day, &month, &year, &studentID, &amount, description) == 6) {
            
            int date = year * 10000 + month * 100 + day;
            
            if (date != currentDate) {
                bc = addBlock(bc);
                currentBlock = bc;
                currentDate = date;
                currentBlock->date = date;
            }
            
            if (currentBlock != NULL) {
                currentBlock->transactions = addTransaction(studentID, amount, description, currentBlock->transactions);
            }
        }
    }
    
    fclose(file);
    printf("transactions imported from %s\n", filename);
    return bc;
}

int getCurrentDate() {
    time_t t = time(NULL);
    struct tm tm = *localtime(&t);
    return (tm.tm_year + 1900) * 10000 + (tm.tm_mon + 1) * 100 + tm.tm_mday;
}

void displayBlockChain(BlockChain bc) {
    printf("\n---------- blockchain ----------\n");
    if (bc == NULL) {
        printf("blockchain is empty!!!\n");
        return;
    }
    
    T_Block *current = bc;
    while (current != NULL) {
        int year = current->date / 10000;
        int month = (current->date % 10000) / 100;
        int day = current->date % 100;
        
        printf("block %d: date %02d/%02d/%04d - %d transactions\n",
               current->blockID, day, month, year,
               countTransactions(current->transactions));
        current = current->next;
    }
}

void displayBlockTransactions(T_Block block) {
    printf("\n---------- transactions in block %d ----------\n", block.blockID);
    int year = block.date / 10000;
    int month = (block.date % 10000) / 100;
    int day = block.date % 100;
    printf("date: %02d/%02d/%04d\n", day, month, year);
    printf("student ID | amount  | description\n");
    printf("----------------------------------\n");
    
    T_Transaction *current = block.transactions;
    if (current == NULL) {
        printf("no transactions in this block\n");
        return;
    }
    
    while (current != NULL) {
        printf("%10d | %7.2f | %s\n", 
               current->studentID, 
               current->amount, 
               current->description);
        current = current->next;
    }
}

void displayStudentDailyTransactions(int idStud, int date, BlockChain bc) {
    printf("\n---------- daily transactions for student %d ----------\n", idStud);
    int year = date / 10000;
    int month = (date % 10000) / 100;
    int day = date % 100;
    printf("date: %02d/%02d/%04d\n", day, month, year);
    printf("amount  | description\n");
    printf("---------------------\n");
    
    T_Block *currentBlock = bc;
    float dailyTotal = 0.0;
    int found = 0;
    
    while (currentBlock != NULL) {
        if (currentBlock->date == date) {
            T_Transaction *currentTransaction = currentBlock->transactions;
            while (currentTransaction != NULL) {
                if (currentTransaction->studentID == idStud) {
                    printf("%7.2f | %s\n", 
                           currentTransaction->amount, 
                           currentTransaction->description);
                    dailyTotal += currentTransaction->amount;
                    found = 1;
                }
                currentTransaction = currentTransaction->next;
            }
            break;
        }
        currentBlock = currentBlock->next;
    }
    
    if (!found) {
        printf("no transactions found for student %d on this date\n", idStud);
    } else {
        printf("total (daily): %.2f EATCoins\n", dailyTotal);
    }
}

void freeBlockChain(BlockChain bc) {
    T_Block *currentBlock = bc;
    while (currentBlock != NULL) {
        T_Transaction *currentTransaction = currentBlock->transactions;
        while (currentTransaction != NULL) {
            T_Transaction *tempTransaction = currentTransaction;
            currentTransaction = currentTransaction->next;
            free(tempTransaction);
        }
        T_Block *tempBlock = currentBlock;
        currentBlock = currentBlock->next;
        free(tempBlock);
    }
}