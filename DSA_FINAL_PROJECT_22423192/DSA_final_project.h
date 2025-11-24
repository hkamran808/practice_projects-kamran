#ifndef DSA_FINAL_PROJECT_H
#define DSA_FINAL_PROJECT_H

typedef struct Transaction {
    int studentID;
    float amount;
    char description[100];
    struct Transaction *next;
} T_Transaction;

typedef struct Block {
    int blockID;
    int date; //YYYYMMDD
    T_Transaction *transactions;
    struct Block *next;
} T_Block;

typedef T_Block *BlockChain;

T_Transaction *addTransaction(int idStud, float amount, char *descr, T_Transaction *listeTransaction);

BlockChain addBlock(BlockChain bc);

float totalTransactionStudentBlock(int idStud, T_Block b);
float soldeStudent(int idStud, BlockChain bc);
void credit(int idStud, float amount, char *descr, BlockChain bc);
int pay(int idStud, float amount, char *descr, BlockChain bc);
void consult(int idStud, BlockChain bc);
int transfer(int idSource, int idDestination, float amount, char *descr, BlockChain bc);
void exportToFile(BlockChain bc, char *filename);
BlockChain importFromFile(char *filename);

void displayBlockChain(BlockChain bc);
void displayBlockTransactions(T_Block block);
void displayStudentDailyTransactions(int idStud, int date, BlockChain bc);
int getCurrentDate();
void freeBlockChain(BlockChain bc);
int countTransactions(T_Transaction *list);

#endif